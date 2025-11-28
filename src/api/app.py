from fastapi.middleware.gzip import GZipMiddleware
from datetime import datetime, timedelta
from pathlib import Path
import os
from fastapi import FastAPI, Depends, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openai import OpenAIError
from .models import (
    TailorRequest, TailorResponse, HealthResponse,
    ApiError, ValidationError, ApiConfig,
    DetailedApiError, ErrorCode, DetailedApiException
)
from .exceptions import TokenLimitError, APIRateLimitError
from services import ResumeService, ResumeServiceInterface
from utils import (
    load_environment,
    CustomLogger,
)
from utils.file_handler import extract_text_from_file
import time
from asyncio import Lock

# Load environment variables
load_environment()

# Initialize config
api_config = ApiConfig()

app = FastAPI(
    title="Resume Tailor API",
    description="API for tailoring resumes using OpenAI GPT",
    version="0.1.0",
)

# Remove middleware from FastAPI initialization and add it properly using add_middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GZip middleware properly
app.add_middleware(
    GZipMiddleware,
    minimum_size=api_config.max_request_size
)

logger = CustomLogger()

# Dependency provider


def get_resume_service() -> ResumeServiceInterface:
    """Provide ResumeService instance"""
    return ResumeService()


@app.get("/ping")
async def ping():
    """Simple ping endpoint to check if API is responding"""
    return {"ping": "pong"}


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint with detailed status"""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        uptime=0.0  # You can track actual uptime if needed
    )


# Add a simple in-memory store for rate limiting
# In production, use Redis or similar
request_counts = {}
request_counts_lock = Lock()


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    async with request_counts_lock:
        """Implement rate limiting using api_config.rate_limit"""
        # Get client IP
        client_ip = request.client.host

        # Get current timestamp
        now = datetime.now()
        minute_window = now.strftime('%Y-%m-%d-%H-%M')

        # Initialize or get request count for this minute
        if minute_window not in request_counts:
            # Cleanup old entries
            current_minute = datetime.now()
            for window in list(request_counts.keys()):
                window_time = datetime.strptime(window, '%Y-%m-%d-%H-%M')
                if window_time < current_minute - timedelta(minutes=1):
                    del request_counts[window]
            request_counts[minute_window] = {}

        if client_ip not in request_counts[minute_window]:
            request_counts[minute_window][client_ip] = 0

        # Check rate limit
        if request_counts[minute_window][client_ip] >= api_config.rate_limit:
            logger.log_error(
                APIRateLimitError(retry_after=60),
                {"client_ip": client_ip}
            )
            raise DetailedApiException(
                error_code=ErrorCode.RATE_LIMIT_EXCEEDED,
                message="Too many requests",
                correlation_id=getattr(request.state, "correlation_id", None),
                retry_after=60,
                suggestion="Please wait a minute before trying again"
            )

        # Increment request count
        request_counts[minute_window][client_ip] += 1

        # Process the request
        response = await call_next(request)
        return response


# Change to handle the exception class
@app.exception_handler(DetailedApiException)
async def detailed_api_error_handler(request: Request, exc: DetailedApiException):
    """Handle DetailedApiException exceptions"""
    response_model = exc.to_response()
    return JSONResponse(
        status_code=429 if exc.error_code == ErrorCode.RATE_LIMIT_EXCEEDED else 500,
        content=response_model.dict()
    )


@app.post(
    "/tailor",
    response_model=TailorResponse,
    responses={
        400: {"model": ValidationError},
        429: {"model": DetailedApiError},
        500: {"model": ApiError}
    }
)
async def tailor_endpoint(
    request: TailorRequest,
    service: ResumeServiceInterface = Depends(get_resume_service)
):
    """Enhanced tailor endpoint with full validation and error handling"""
    logger.set_request_context()  # Generate new request ID
    start_time = time.time()

    try:
        # Log the incoming request
        logger.log_request(request.model_dump())

        # Process the request
        result = await service.tailor_resume(
            resume_text=request.resume_text,
            job_description=request.job_description,
            tone=request.tone
        )

        # Log performance
        end_time = time.time()
        processing_time = end_time - start_time

        # Create response with usage information
        response = TailorResponse(
            tailored_resume=result["content"],
            metadata={
                "processing_time": processing_time,
                "timestamp": datetime.utcnow().isoformat(),
                "model": os.getenv('MODEL_NAME', 'gpt-4'),
                "tokens_used": result["usage"]["total_tokens"],
                "cost_usd": result["usage"]["cost_usd"],
                "input_tokens": result["usage"]["input_tokens"],
                "output_tokens": result["usage"]["output_tokens"]
            }
        )

        if request.save_output:
            # Create timestamp for unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Ensure output directory exists
            output_dir = Path(__file__).parent.parent.parent / \
                "data" / "output"
            output_dir.mkdir(parents=True, exist_ok=True)

            # Save file
            output_path = output_dir / f"tailored_resume_{timestamp}.txt"
            output_path.write_text(result["content"])

            # Add file path to response
            response.saved_to = str(output_path)

        return response

    except OpenAIError as e:
        raise DetailedApiException(
            error_code=ErrorCode.API_ERROR,
            message=str(e),
            correlation_id=request.correlation_id,
            suggestion="Check API key or try again later"
        )

    except APIRateLimitError as e:
        logger.log_error(e, request.model_dump())
        raise DetailedApiException(
            error_code=ErrorCode.RATE_LIMIT_EXCEEDED,
            message="Rate limit exceeded",
            correlation_id=request.correlation_id,
            retry_after=e.retry_after,
            suggestion="Please wait before making more requests"
        )

    except Exception as e:
        logger.log_error(e, {"request": request.dict()})
        raise

    except IOError as e:
        raise DetailedApiException(
            error_code=ErrorCode.FILE_SYSTEM_ERROR,
            message="Failed to save output file",
            correlation_id=request.correlation_id
        )

    except TokenLimitError as e:
        logger.log_error(e, request.model_dump())
        raise DetailedApiException(
            error_code=ErrorCode.TOKEN_LIMIT_EXCEEDED,
            message="Input text too long",
            suggestion="Try reducing input text length"
        )


@app.post(
    "/tailor-upload",
    response_model=TailorResponse,
    responses={
        400: {"model": ValidationError},
        429: {"model": DetailedApiError},
        500: {"model": ApiError}
    },
    summary="Upload Resume and Job Description Files",
    description="""
    Upload your resume and job description as files for AI-powered tailoring.
    
    **Supported formats:** PDF, DOCX, TXT
    
    **What you'll get:**
    - Tailored resume matching the job description
    - Optimized keywords and phrases
    - Professional formatting maintained
    """
)
async def tailor_upload_endpoint(
    Resume: UploadFile = File(
        ...,
        description="Upload the Resume file",
        title="Resume File",
        openapi_examples={
            "example1": {
                "summary": "PDF Resume",
                "value": "my_resume.pdf"
            }
        }
    ),
    JD: UploadFile = File(
        ...,
        description="Upload the Job Description file",
        title="Job Description File",
        openapi_examples={
            "example1": {
                "summary": "Text Job Description",
                "value": "job_description.txt"
            }
        }
    ),
    Tone: str = Form(
        default="professional",
        description="Tone for the tailored resume",
        title="Tone",
        examples=["professional", "casual", "academic"]
    ),
    Save: bool = Form(
        default=True,
        description="Save the tailored resume to output folder",
        title="Save Output"
    ),
    service: ResumeServiceInterface = Depends(get_resume_service)
):
    """
    Upload files to tailor resume.

    Accepts:
    - Resume: Your resume in PDF, DOCX, or TXT format
    - JD: Job description in PDF, DOCX, or TXT format
    - Tone: professional, casual, or academic
    - Save: Whether to save the result
    """
    start_time = time.time()

    try:
        # Validate file types
        allowed_extensions = {'.pdf', '.docx', '.txt'}
        resume_ext = Path(Resume.filename).suffix.lower()
        job_ext = Path(JD.filename).suffix.lower()

        if resume_ext not in allowed_extensions:
            raise DetailedApiException(
                error_code=ErrorCode.VALIDATION_ERROR,
                message=f"Resume file type {resume_ext} not supported. Use PDF, DOCX, or TXT.",
                suggestion="Upload a file with .pdf, .docx, or .txt extension"
            )

        if job_ext not in allowed_extensions:
            raise DetailedApiException(
                error_code=ErrorCode.VALIDATION_ERROR,
                message=f"Job description file type {job_ext} not supported. Use PDF, DOCX, or TXT.",
                suggestion="Upload a file with .pdf, .docx, or .txt extension"
            )

        # Extract text from files
        logger.logger.info(f"Processing resume file: {Resume.filename}")
        resume_text = await extract_text_from_file(Resume.file, Resume.filename)

        logger.logger.info(f"Processing job file: {JD.filename}")
        job_text = await extract_text_from_file(JD.file, JD.filename)

        # Validate extracted text
        if len(resume_text.strip()) < 100:
            raise DetailedApiException(
                error_code=ErrorCode.VALIDATION_ERROR,
                message="Resume text too short. Must be at least 100 characters.",
                suggestion="Upload a complete resume file"
            )

        if len(job_text.strip()) < 50:
            raise DetailedApiException(
                error_code=ErrorCode.VALIDATION_ERROR,
                message="Job description too short. Must be at least 50 characters.",
                suggestion="Upload a complete job description"
            )

        # Process the request
        result = await service.tailor_resume(
            resume_text=resume_text,
            job_description=job_text,
            tone=Tone
        )

        # Log performance
        end_time = time.time()
        processing_time = end_time - start_time

        response = TailorResponse(
            tailored_resume=result["content"],
            metadata={
                "processing_time": processing_time,
                "timestamp": datetime.utcnow().isoformat(),
                "resume_file": Resume.filename,
                "job_file": JD.filename,
                "model": os.getenv('MODEL_NAME', 'gpt-4'),
                "tokens_used": result["usage"]["total_tokens"],
                "cost_usd": result["usage"]["cost_usd"],
                "input_tokens": result["usage"]["input_tokens"],
                "output_tokens": result["usage"]["output_tokens"]
            }
        )

        if Save:
            # Create timestamp for unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Ensure output directory exists
            output_dir = Path(__file__).parent.parent.parent / \
                "data" / "output"
            output_dir.mkdir(parents=True, exist_ok=True)

            # Save file
            output_path = output_dir / f"tailored_resume_{timestamp}.txt"
            output_path.write_text(result["content"])

            # Add file path to response
            response.saved_to = str(output_path)

        return response

    except ValueError as e:
        raise DetailedApiException(
            error_code=ErrorCode.VALIDATION_ERROR,
            message=str(e),
            suggestion="Check file format and try again"
        )

    except DetailedApiException:
        # Re-raise our custom exceptions
        raise

    except Exception as e:
        # Safely get filenames if they exist
        context = {}
        try:
            context["resume_file"] = Resume.filename if Resume else "unknown"
            context["job_file"] = JD.filename if JD else "unknown"
        except:
            pass

        logger.log_error(e, context)
        raise DetailedApiException(
            error_code=ErrorCode.API_ERROR,
            message=f"Error processing files: {str(e)}",
            suggestion="Check file format and content"
        )
