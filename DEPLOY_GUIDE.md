# 🚀 Render.com Deployment Guide

## ⚠️ CRITICAL: Security Actions Completed ✅

✅ **API Key Removed** - Exposed OpenAI API key has been removed from code
✅ **Production Dockerfile** - Updated for secure, multi-worker deployment  
✅ **Security Validation** - Added production settings validation
✅ **Enhanced Health Check** - Added dependency monitoring

## 🔧 Deploy to Render.com

### 1. Create New Web Service
1. Go to [Render.com](https://render.com) 
2. Click "New +" → "Web Service"
3. Connect your GitHub repository: `aravindswamy246/Resume-Tailor`

### 2. Configure Environment Variables ⚠️ IMPORTANT
In Render dashboard, add these environment variables:

```bash
# 🔑 REQUIRED - Generate a NEW API key from OpenAI
OPENAI_API_KEY=sk-proj-YOUR_NEW_KEY_HERE

# Optional (with defaults)
MODEL_NAME=gpt-4
MAX_TOKENS=2000
TEMPERATURE=0.7
LOG_LEVEL=INFO

# Production flags
RENDER=true
ALLOWED_HOSTS=your-app-name.onrender.com
```

### 3. Service Configuration
- **Environment**: Docker
- **Branch**: master  
- **Docker Command**: Uses CMD from Dockerfile (automatic)
- **Health Check Path**: `/health`
- **Auto Deploy**: ✅ Enabled

### 4. Production Features Enabled ✅

**Security:**
- Non-root user in container
- Environment variable validation
- CORS restrictions in production
- TrustedHost middleware
- No debug mode in production

**Performance:**
- 4 worker processes (uvicorn)
- GZip compression
- Optimized Docker layers

**Monitoring:**
- Enhanced `/health` endpoint
- Dependency status checks
- Structured logging

## 🔍 Verify Deployment

### 1. Basic Connectivity Tests
```bash
# Health check (most important)
curl https://your-app.onrender.com/health
# Expected: {"status":"healthy","version":"0.1.0",...}

# Simple ping
curl https://your-app.onrender.com/ping
# Expected: {"ping":"pong"}
```

### 2. Interactive API Testing
```bash
# Open Swagger UI in browser
https://your-app.onrender.com/docs

# OpenAPI specification
https://your-app.onrender.com/openapi.json
```

### 3. Resume Tailoring Tests
```bash
# Test text input
curl -X POST "https://your-app.onrender.com/tailor" \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Python Developer with FastAPI experience",
    "resume_text": "Software engineer with Python skills..."
  }'

# Test file upload
curl -X POST "https://your-app.onrender.com/tailor-file" \
  -F "job_description=Python Developer position" \
  -F "resume_file=@resume.pdf"
```

### 4. Monitor Deployment Logs
In Render dashboard → Your Service → Logs tab, look for:
```
✅ Application startup complete
✅ Uvicorn running on http://0.0.0.0:10000 (4 workers)
✅ Production settings validated
```

## 🚨 Next Steps

1. **REGENERATE OpenAI API Key** - The old key is compromised
2. **Set Environment Variables** in Render dashboard
3. **Update ALLOWED_HOSTS** with your actual Render domain
4. **Test API endpoints** after deployment
5. **Monitor logs** for any errors

## 📊 Production Checklist

- ✅ API key security fixed
- ✅ Docker production-ready
- ✅ Health monitoring enabled
- ✅ Multi-worker deployment
- ✅ Error handling improved
- ✅ CORS properly configured
- ⏳ **TODO**: Set environment variables in Render
- ⏳ **TODO**: Generate new OpenAI API key