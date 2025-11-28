# Docker Quick Reference

## Daily Development Workflow

### Starting Development
```bash
# Start container (one time)
docker compose up -d

# Watch logs in real-time
docker compose logs -f
```

### Making Code Changes
1. Edit any `.py` file in `src/`
2. Save the file
3. Wait 1-2 seconds for auto-reload
4. Test your changes

**No rebuild needed!** The container automatically detects changes and reloads.

## When to Rebuild

### Requirements Changed
```bash
./rebuild.sh
```
Run this when you:
- Add/remove packages in `requirements.txt`
- Update package versions
- Change `Dockerfile`
- Change `docker-compose.yml`

### Manual Rebuild
```bash
docker compose down
docker compose build
docker compose up -d
```

## Common Commands

### Container Management
```bash
# Start container
docker compose up -d

# Stop container
docker compose down

# Restart container (keeps same image)
docker compose restart

# View running containers
docker ps

# View all containers (including stopped)
docker ps -a
```

### Logs
```bash
# View recent logs
docker compose logs

# Follow logs (real-time) - RECOMMENDED to see cost tracking
docker compose logs -f

# View last 50 lines
docker compose logs --tail=50

# View logs for specific time
docker compose logs --since 5m

# Filter for cost information
docker compose logs -f | grep -E "(OpenAI|Cost|Token)"
```

**What to look for in logs:**
- `OpenAI API Call` - Shows token usage and cost per request
- `Input Tokens` - Number of tokens in your prompt
- `Output Tokens` - Number of tokens in the response
- `Cost` - Estimated cost in USD for the API call

### Health Checks
```bash
# Quick health check
curl http://localhost:8000/health

# Ping endpoint
curl http://localhost:8000/ping

# Check from within container
docker exec resume-tailor curl http://localhost:8000/health
```

### Debugging
```bash
# Enter container shell
docker exec -it resume-tailor /bin/bash

# Check container resource usage
docker stats resume-tailor

# Inspect container details
docker inspect resume-tailor

# View container processes
docker top resume-tailor
```

### Cleanup
```bash
# Remove unused images
docker image prune -f

# Remove all unused resources
docker system prune -f

# Remove everything (including volumes)
docker system prune -a -f --volumes

# Remove specific container
docker rm resume-tailor

# Remove specific image
docker rmi p1-resume-tailor
```

## Troubleshooting

### Port Already in Use
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
docker compose up -d -e API_PORT=8080
```

### Container Won't Start
```bash
# Check logs for errors
docker compose logs --tail=100

# Check if image exists
docker images | grep resume-tailor

# Rebuild from scratch
docker compose down -v
docker compose build --no-cache
docker compose up -d
```

### Hot-Reload Not Working
```bash
# Check if volume is mounted
docker inspect resume-tailor | grep -A 5 Mounts

# Restart container
docker compose restart

# If still not working, rebuild
./rebuild.sh
```

### Environment Variables Not Loading
```bash
# Check .env file exists
cat .env

# Verify variables in container
docker exec resume-tailor env | grep OPENAI

# Restart after .env changes
docker compose down
docker compose up -d
```

### API Returning Errors
```bash
# Check API logs
docker compose logs -f

# Test health endpoint
curl http://localhost:8000/health

# Check OpenAI API key
docker exec resume-tailor env | grep OPENAI_API_KEY

# Verify Python packages
docker exec resume-tailor pip list
```

## File Upload Testing

### Using curl
```bash
# Upload PDF resume and TXT job description
curl -X POST "http://localhost:8000/tailor-upload" \
     -F "Resume=@data/input/resumes/resume.pdf" \
     -F "JD=@data/input/jobs/job.txt" \
     -F "Tone=professional" \
     -F "Save=true"

# The response includes cost information
# Example output:
# {
#   "tailored_resume": "...",
#   "metadata": {
#     "tokens_used": 1801,
#     "cost_usd": 0.082500,
#     "input_tokens": 1234,
#     "output_tokens": 567,
#     "model": "gpt-4"
#   }
# }
```

### Using Swagger UI
1. Open http://localhost:8000/docs
2. Find `/tailor-upload` endpoint
3. Click "Try it out"
4. Upload files using file pickers
5. Fill in parameters
6. Click "Execute"
7. Check response for cost information in metadata

## Performance Monitoring

### Check Container Stats
```bash
# Real-time stats
docker stats resume-tailor

# One-time stats
docker stats --no-stream resume-tailor
```

### Check API Response Times
```bash
# Time a request
time curl -X POST "http://localhost:8000/tailor" \
     -H "Content-Type: application/json" \
     -d '{"resume_text":"test","job_description":"test"}'
```

## Best Practices

1. **Use hot-reload for development**
   - No need to rebuild for code changes
   - Saves time and keeps workflow smooth

2. **Use rebuild.sh for dependency changes**
   - Clean way to update after requirements.txt changes
   - Includes cleanup and health checks

3. **Monitor logs during development**
   - Keep `docker compose logs -f` running
   - Catch errors immediately
   - Track API costs in real-time

4. **Regular cleanup**
   - Run `docker image prune -f` weekly
   - Prevents disk space issues

5. **Use health checks before testing**
   - Always verify container is healthy
   - Check logs if health check fails

6. **Track API costs**
   - Monitor logs for cost information
   - Check response metadata for per-request costs
   - Visit https://platform.openai.com/usage for actual billing
