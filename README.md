# Resume Tailor

AI-powered resume tailoring tool that customizes your resume to match job descriptions using OpenAI's GPT API.

## Features
- Automated resume tailoring based on job descriptions
- OpenAI GPT integration for intelligent content generation
- RESTful API with FastAPI
- **File upload support** (PDF, DOCX, TXT) via Swagger UI
- **Token usage and cost tracking** per API call
- Real-time cost calculation with detailed metrics
- File monitoring and logging support
- Configurable model parameters
- Rate limiting and request validation
- Docker containerization with hot-reload for development
- Comprehensive error handling and logging
- Interactive API documentation with Swagger UI

## Prerequisites
- Python 3.8 or higher
- OpenAI API key
- macOS/Linux/Windows (cross-platform support)
- Docker (optional, for containerized deployment)

## Project Structure
```
p1/
├── src/
│   ├── api/                  # FastAPI application
│   │   ├── app.py           # Main API application
│   │   ├── server.py        # Server runner
│   │   ├── exceptions.py    # Custom exceptions
│   │   └── models/          # Pydantic models
│   ├── resume_tailor/       # Core tailoring logic
│   ├── services/            # Service layer
│   │   ├── base.py         # Base service
│   │   └── resume_service.py
│   └── utils/              # Utility functions
│       ├── logger.py       # Enhanced logging
│       ├── file_handler.py
│       ├── env_loader.py
│       └── api_config.py
├── data/
│   ├── input/              # Input resumes and job descriptions
│   │   ├── resumes/
│   │   └── jobs/
│   └── output/             # Generated tailored resumes
├── logs/                   # Application logs
├── tests/                  # Test suite
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
└── setup.py              # Package setup
```

## Installation

### Option 1: Local Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd p1
```

2. Create and activate virtual environment:
```bash
python3 -m venv env_p1
source env_p1/bin/activate  # On Windows: env_p1\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

5. Install the package in development mode:
```bash
pip install -e .
```

### Option 2: Docker Installation

1. Install Docker Desktop:
   - Download from: https://www.docker.com/products/docker-desktop
   - Follow installation instructions for your OS

2. Clone the repository:
```bash
git clone <repository-url>
cd p1
```

3. Build the Docker image:
```bash
docker build -t resume-tailor:latest .
```

4. Run the container:
```bash
docker run -d \
  --name resume-tailor \
  -p 8000:8000 \
  -v $(pwd)/logs:/app/logs \
  -e OPENAI_API_KEY=your_api_key_here \
  resume-tailor:latest
```

### Option 3: Docker Compose (Recommended)

1. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

2. Start the application:
```bash
docker compose up -d
```

3. Stop the application:
```bash
docker compose down
```

4. Rebuild after changes (quick rebuild script):
```bash
./rebuild.sh
```

**Development Mode:**
The Docker container runs with hot-reload enabled. Simply edit Python files in `src/` and save - the server will automatically restart with your changes in 1-2 seconds!

## Configuration

### Environment Variables
Create a `.env` file with the following variables:
```env
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4
MAX_TOKENS=2000
TEMPERATURE=0.7
LOG_LEVEL=INFO
```

### API Configuration
- **Rate Limiting**: 10 requests per minute per IP
- **Max Workers**: 4 (configurable in Dockerfile)
- **Port**: 8000 (default)
- **Host**: 0.0.0.0 (all interfaces)

## Usage

### Command Line Interface

1. Place your resume in `data/input/resumes`
2. Add job description to `data/input/jobs`
3. Run the tailoring script:
```bash
python -m src.main data/input/resumes/Test_Resume.txt data/input/jobs/JD.txt --tone professional
```
4. Find tailored resume in `data/output`

### API Usage

#### Starting the API Server

**Local Development:**
```bash
python src/api/server.py
```

**Docker:**
```bash
docker start resume-tailor
```

**Docker Compose:**
```bash
docker compose up -d
```

#### Available Endpoints

- `GET /` - API root information
- `GET /ping` - Basic health check
- `GET /health` - Detailed health status with dependencies
- `POST /tailor` - Tailor resume with JSON request body
- `POST /tailor-upload` - **NEW:** Upload resume and job description files (PDF, DOCX, TXT)

#### API Documentation
Once the server is running, access interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

#### Example API Calls

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Tailor Resume (JSON):**
```bash
curl -X POST "http://localhost:8000/tailor" \
     -H "Content-Type: application/json" \
     -d '{
           "resume_text": "Your resume content here",
           "job_description": "Job description here",
           "tone": "professional",
           "save_output": true
         }'
```

**Tailor Resume (File Upload):**
```bash
curl -X POST "http://localhost:8000/tailor-upload" \
     -F "resume_file=@/path/to/resume.pdf" \
     -F "job_file=@/path/to/job_description.txt" \
     -F "tone=professional" \
     -F "save_output=true"
```

**Using Python:**
```python
import requests

# JSON method
response = requests.post(
    "http://localhost:8000/tailor",
    json={
        "resume_text": "Your resume content",
        "job_description": "Job description",
        "tone": "professional",
        "save_output": True
    }
)
result = response.json()
print(f"Tailored Resume: {result['tailored_resume']}")
print(f"Tokens Used: {result['metadata']['tokens_used']}")
print(f"Cost: ${result['metadata']['cost_usd']:.6f}")

# File upload method
with open('resume.pdf', 'rb') as resume, open('job.txt', 'rb') as job:
    response = requests.post(
        "http://localhost:8000/tailor-upload",
        files={
            'resume_file': resume,
            'job_file': job
        },
        data={
            'tone': 'professional',
            'save_output': True
        }
    )
    result = response.json()
    print(f"Tailored Resume: {result['tailored_resume']}")
    print(f"Tokens Used: {result['metadata']['tokens_used']}")
    print(f"Cost: ${result['metadata']['cost_usd']:.6f}")
```

### API Response Format

The API returns detailed usage metrics in the response:

```json
{
  "tailored_resume": "Your tailored resume content...",
  "metadata": {
    "processing_time": 5.234,
    "timestamp": "2025-11-09T12:34:56.789",
    "model": "gpt-4",
    "tokens_used": 1801,
    "cost_usd": 0.082500,
    "input_tokens": 1234,
    "output_tokens": 567
  },
  "saved_to": "/app/data/output/tailored_resume_20251109_123456.txt"
}
```

## Docker Commands

### Building the Image
```bash
docker build -t resume-tailor:latest .
```

### Running the Container
```bash
# Basic run
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key resume-tailor:latest

# With environment variables and volume mounting
docker run -d \
  --name resume-tailor \
  -p 8000:8000 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/data:/app/data \
  -e OPENAI_API_KEY=your_key \
  resume-tailor:latest
```

### Managing Containers
```bash
# Stop container
docker stop resume-tailor

# Start container
docker start resume-tailor

# View logs
docker logs resume-tailor

# View logs in real-time
docker logs -f resume-tailor

# View running containers
docker ps

# Remove container
docker rm resume-tailor

# Remove image
docker rmi resume-tailor:latest
```

### Using Docker Compose
```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs (to see cost tracking)
docker compose logs -f

# View recent logs
docker compose logs --tail=100

# Restart after code changes (hot-reload enabled, no rebuild needed)
# Just save your Python files - changes are detected automatically!

# Rebuild after requirements.txt changes
./rebuild.sh
```

## Cost Tracking and Monitoring

### Viewing API Costs

**Container Logs:**
```bash
docker compose logs -f
```

You'll see entries like:
```
INFO: OpenAI API Call - Model: gpt-4, Input Tokens: 1234, Output Tokens: 567, Total Tokens: 1801, Cost: $0.082500
```

**Log Files:**
```bash
# View persistent logs
tail -f logs/resume_tailor.log

# Check logs directory
ls -lh logs/
```

**API Response:**
Every API call returns cost information in the metadata:
```json
{
  "metadata": {
    "tokens_used": 1801,
    "cost_usd": 0.082500,
    "input_tokens": 1234,
    "output_tokens": 567,
    "model": "gpt-4"
  }
}
```

### Cost Calculation

Pricing is calculated based on current OpenAI rates (per 1K tokens):

|     Model     | Input (per 1K)  | Output (per 1K) |
|---------------|-----------------|-----------------|
| GPT-4         | $0.03           | $0.06           |
| GPT-4-turbo   | $0.01           | $0.03           |
| GPT-4o        | $0.0025         | $0.01           |
| GPT-3.5-turbo | $0.0005         | $0.0015         |

**Example Cost:**
- Input: 1,234 tokens × $0.03 / 1000 = $0.037020
- Output: 567 tokens × $0.06 / 1000 = $0.034020
- **Total: $0.071040**

### Monitoring OpenAI Usage

Check your actual OpenAI usage and costs at:
https://platform.openai.com/usage

# Or manually rebuild
docker compose down
docker compose build
docker compose up -d

# Remove all containers and volumes
docker compose down -v
```

### Hot-Reload Development Workflow

The Docker container is configured with hot-reload for faster development:

1. **Start the container once:**
```bash
docker compose up -d
```

2. **Edit Python files in `src/`** - Changes are detected automatically!

3. **Watch reload in action:**
```bash
docker compose logs -f
# You'll see: "StatReload detected changes... Reloading..."
```

4. **Only rebuild when needed:**
   - Changed `requirements.txt`: Run `./rebuild.sh`
   - Changed `Dockerfile` or `docker-compose.yml`: Run `./rebuild.sh`
   - Changed `.py` files: No rebuild needed! Just save.

### Rebuild Script

Use the convenient rebuild script for full rebuilds:
```bash
./rebuild.sh
```

This script will:
1. Stop the container
2. Ask for confirmation to remove old images
3. Build a fresh image
4. Start the container
5. Check health status

## Logging

The application uses comprehensive logging with:
- **Request tracking**: Unique request IDs for tracing
- **Performance monitoring**: Request duration and status tracking
- **Error logging**: Detailed error information with stack traces
- **Log rotation**: Automatic log file management (10MB max, 5 backups)

Logs are stored in:
- Local: `logs/resume_tailor.log`
- Docker: Mounted volume at `/app/logs`

View logs in real-time:
```bash
# Local
tail -f logs/resume_tailor.log

# Docker
docker logs -f resume-tailor

# Docker Compose
docker compose logs -f
```

## Error Handling

The API includes comprehensive error handling:
- **ValidationError**: Invalid request data (400)
- **APIRateLimitError**: Too many requests (429)
- **TokenLimitError**: Input text too long (400)
- **OpenAIError**: AI service failures (500)
- **IOError**: File handling issues (500)

Each error includes:
- Error code
- Detailed message
- Correlation ID for tracking
- Suggested remediation

## Development

### Setup Development Environment
```bash
# Install with dev dependencies
pip install -r requirements.txt

# Install testing dependencies
pip install pytest pytest-asyncio pytest-cov httpx

# Run tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html

# Format code
black src/

# Lint code
flake8 src/
```

### Running Tests
```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py

# Run with coverage report
pytest tests/ --cov=src --cov-report=term-missing
```

### Code Style
- Follow PEP 8 style guide
- Use type hints for function signatures
- Add docstrings for all public functions and classes
- Keep functions small and focused

### Adding New Features
1. Create feature branch
2. Implement feature with tests
3. Update documentation
4. Submit pull request

## Troubleshooting

### Common Issues

**Docker build fails:**
- Ensure Docker Desktop is running
- Check internet connection for downloading base image
- Verify sufficient disk space

**API returns 500 errors:**
- Verify OpenAI API key is set correctly
- Check API key has sufficient credits
- Review logs for detailed error messages

**Rate limiting:**
- Default: 10 requests/minute per IP
- Adjust in `src/api/app.py` if needed

**Port already in use:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process or use different port
docker run -p 8080:8000 resume-tailor:latest
```

**Module import errors:**
- Ensure PYTHONPATH is set: `export PYTHONPATH=/app/src`
- In Docker, this is automatically configured

## Security Considerations

- API keys are loaded from environment variables (never hardcoded)
- Non-root user runs the application in Docker
- Input validation with Pydantic models
- Rate limiting prevents abuse
- No sensitive data logged
- CORS configured for security

## Performance

- Async operations for I/O-bound tasks
- Multiple Uvicorn workers (4 by default)
- Connection pooling for HTTP clients
- Efficient error handling with minimal overhead
- Request/response caching where applicable

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Email: aravind.adari@gmail.com

## Changelog

### Version 0.1.1 - 2025-11-09
- **Token usage and cost tracking** per API call
- Real-time cost calculation with detailed metrics
- Enhanced API response with usage data (tokens, cost)
- Fixed DOCX file upload compatibility issues
- Fixed error handling with correct ErrorCode enums
- Improved logging with cost information
- **Production readiness improvements**:
  - Added centralized configuration management
  - Created comprehensive production checklist
  - Added test template and testing dependencies
  - Added `pydantic-settings`, `pytest`, `pytest-asyncio`, `httpx`

### Version 0.1.0 - 2025-11-09
- Initial release
- FastAPI REST API
- Docker support with hot-reload for development
- Enhanced logging with request tracking
- Rate limiting
- Comprehensive error handling
- Interactive API documentation
- CLI interface
- Service layer architecture
- **File upload endpoint** for PDF, DOCX, and TXT files
- Automatic text extraction from documents
- Rebuild script for easy container management
- Volume mounting for source code hot-reload
- Rate limiting
- Comprehensive error handling
- Interactive API documentation
- CLI interface
- Service layer architecture
- **File upload endpoint** for PDF, DOCX, and TXT files
- Automatic text extraction from documents
- Rebuild script for easy container management
- Volume mounting for source code hot-reload