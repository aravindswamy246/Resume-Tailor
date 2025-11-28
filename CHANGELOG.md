# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1] - 2025-11-09

### Added
- **Token Usage and Cost Tracking**
  - Real-time token counting (input, output, total tokens)
  - Cost calculation per API call based on model pricing
  - Detailed cost logging in container logs
  - Cost information included in API response metadata
  - Support for multiple GPT models (GPT-4, GPT-4-turbo, GPT-4o, GPT-3.5-turbo)

- **Production Readiness**
  - Created `PRODUCTION_CHECKLIST.md` with comprehensive deployment guide
  - Added centralized configuration management (`src/config.py`)
  - Added API module initialization (`src/api/__init__.py`)
  - Created test template (`tests/test_api.py`) for unit and integration tests
  - Added `pydantic-settings>=2.0.3` for settings management
  - Added testing dependencies: `pytest>=7.4.0`, `pytest-asyncio>=0.21.0`, `pytest-cov>=4.1.0`

### Changed
- Enhanced API response to include detailed usage metrics:
  - `tokens_used`: Total tokens consumed
  - `input_tokens`: Prompt tokens
  - `output_tokens`: Completion tokens
  - `cost_usd`: Estimated cost in USD
  - `model`: Model used for generation
- Modified service layer to return dict with content and usage data
- Updated both `/tailor` and `/tailor-upload` endpoints with cost tracking

### Fixed
- **File Upload Issues**
  - Fixed `SpooledTemporaryFile` compatibility with PyPDF2 and python-docx
  - Added `BytesIO` wrapper for seekable file operations
  - Resolved DOCX upload failures
- **Error Handling**
  - Changed `ErrorCode.INTERNAL_ERROR` to `ErrorCode.API_ERROR` (correct enum value)
  - Fixed undefined variable errors in exception handlers
  - Added safe context gathering in error logging
- **Docker Health Checks**
  - Disabled health checks to reduce log noise (optional, configurable)
  - Health endpoint remains available for manual checks

### Technical Details
- Added pricing table for GPT models in `tailor.py`
- Implemented `calculate_cost()` function with per-1K-token pricing
- Enhanced logging with `CustomLogger` for cost tracking
- Response format change: service returns `{"content": str, "usage": dict}`

## [0.1.0] - 2025-11-09

### Added
- **File Upload Endpoint** (`POST /tailor-upload`)
  - Support for PDF, DOCX, and TXT file uploads
  - Automatic text extraction from uploaded documents
  - File validation and error handling
  - Integrated with Swagger UI for easy testing

- **Docker Hot-Reload Support**
  - Source code volume mounting for development
  - Automatic server restart on code changes
  - No rebuild needed for Python file modifications
  - Faster development iteration

- **Rebuild Script** (`rebuild.sh`)
  - Automated container rebuild workflow
  - Confirmation prompt before cleaning old images
  - Health check verification after rebuild
  - Single command for full rebuild cycle

- **Enhanced Dependencies**
  - `python-multipart>=0.0.9` for file upload support
  - Updated `uvicorn>=0.34.0` with standard extras
  - `PyPDF2>=3.0.0` for PDF text extraction
  - `python-docx>=1.2.0` for DOCX text extraction

### Changed
- Updated Dockerfile to use `--reload` flag for development
- Modified docker-compose.yml to mount source code directory
- Enhanced API documentation with better file upload examples
- Improved Swagger UI display for file upload fields with MIME types

### Fixed
- Pydantic V2 compatibility (using `json_schema_extra` instead of `schema_extra`)
- Environment variable handling in Docker (OPENAI_API_KEY)
- Container health check uptime field
- File handler for async operations

### Documentation
- Updated README.md with file upload examples
- Added hot-reload development workflow instructions
- Documented rebuild script usage
- Added curl and Python examples for file uploads
- Updated setup.py and pyproject.toml with new dependencies

### Technical Details
- FastAPI 0.120.0 with file upload support
- Async file handling with aiofiles
- Text extraction utilities in `src/utils/file_handler.py`
- Validation for file types and content length
- Support for multiple file formats in single endpoint

## Development Workflow Changes

### Before
```bash
# Every change required full rebuild
docker compose down
docker compose build
docker compose up -d
```

### After
```bash
# One-time setup
docker compose up -d

# Edit Python files - automatic reload!
# Just save and wait 1-2 seconds

# Only rebuild when needed (requirements.txt, Dockerfile changes)
./rebuild.sh
```

## API Changes

### New Endpoints
- `POST /tailor-upload` - Upload resume and job description files

### Request Format
```bash
curl -X POST "http://localhost:8000/tailor-upload" \
     -F "resume_file=@resume.pdf" \
     -F "job_file=@job.txt" \
     -F "tone=professional" \
     -F "save_output=true"
```

### Supported File Types
- PDF (`.pdf`)
- Microsoft Word (`.docx`)
- Plain Text (`.txt`)

## Breaking Changes
None - All existing endpoints remain unchanged.

## Migration Guide
No migration needed. This is the initial release with all features included.

## Security Notes
- File uploads are validated for type and size
- Text extraction happens in memory (no disk writes)
- Temporary files are automatically cleaned up
- File content validation before processing

## Performance Improvements
- Hot-reload reduces development iteration time from ~30s to ~2s
- Async file handling for better concurrency
- In-memory text extraction (no disk I/O)

## Known Issues
None at this time.

## Upcoming Features
- Request ID tracking in logs
- GPT token usage and cost tracking
- Prompt logging for debugging
- Structured logging with correlation IDs
- Support for additional file formats (RTF, ODT)
- Batch processing endpoint
- Resume template selection
