# AWIES Docker Deployment Guide

Complete guide for deploying AWIES using Docker and Docker Compose.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- At least 2GB RAM
- OpenAI or Gemini API key

## Quick Start

### 1. Clone and Navigate to Project

```bash
cd /home/user/rewrite
```

### 2. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.docker.example .env

# Edit the .env file with your API credentials
nano .env
```

**Required Configuration:**

```bash
# For OpenAI
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-api-key-here
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o

# OR for Gemini
LLM_PROVIDER=gemini
LLM_API_KEY=your-gemini-api-key
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta
LLM_MODEL=gemini-2.0-flash-001
```

### 3. Build and Start Services

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Configuration Options

### Port Configuration

Change ports in `.env`:

```bash
BACKEND_PORT=8000   # Backend API port
FRONTEND_PORT=3000  # Frontend web interface port
```

### LLM Provider Options

#### Option 1: OpenAI

```bash
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o
```

**Supported Models:**
- `gpt-4o` (recommended)
- `gpt-4-turbo`
- `gpt-4`
- `gpt-3.5-turbo`

#### Option 2: OpenAI-Compatible APIs (e.g., OhMyGPT)

```bash
LLM_PROVIDER=openai
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://api.ohmygpt.com/v1
LLM_MODEL=gpt-4o
```

#### Option 3: Google Gemini

```bash
LLM_PROVIDER=gemini
LLM_API_KEY=your-gemini-api-key
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta
LLM_MODEL=gemini-2.0-flash-001
```

**Supported Models:**
- `gemini-2.0-flash-001` (recommended, fast)
- `gemini-1.5-pro`
- `gemini-1.5-flash`

### Logging Level

```bash
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## Docker Commands

### Start Services

```bash
# Start in foreground
docker-compose up

# Start in background (detached)
docker-compose up -d

# Rebuild and start
docker-compose up -d --build
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Update Configuration

After changing `.env`:

```bash
# Restart to apply new environment variables
docker-compose down
docker-compose up -d
```

### Update Application Code

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

## Health Checks

### Check Service Health

```bash
# Check all services
docker-compose ps

# Check backend health
curl http://localhost:8000/api/health

# Check frontend
curl http://localhost:3000
```

### Service Status

- ✅ `Up (healthy)` - Service is running properly
- 🔄 `Up (health: starting)` - Service is starting
- ❌ `Up (unhealthy)` - Service has issues

## Troubleshooting

### Backend Won't Start

```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. Missing API key
# 2. Invalid model name
# 3. Network connectivity issues
```

### Frontend Can't Connect to Backend

```bash
# Check if backend is healthy
curl http://localhost:8000/api/health

# Verify backend is accessible from frontend container
docker-compose exec frontend wget -O- http://backend:8000/api/health
```

### API Key Issues

```bash
# Verify environment variables are loaded
docker-compose exec backend env | grep LLM

# Check if API key is set
docker-compose exec backend python -c "from app.core.config import settings; print(settings.llm_api_key[:10])"
```

### Out of Memory

```bash
# Check resource usage
docker stats

# Increase Docker memory limit in Docker settings
# Recommended: At least 2GB RAM
```

### Port Already in Use

```bash
# Change ports in .env
BACKEND_PORT=8001
FRONTEND_PORT=3001

# Restart services
docker-compose down
docker-compose up -d
```

## Production Deployment

### Security Recommendations

1. **Use secrets management** for API keys
2. **Enable HTTPS** with a reverse proxy (nginx/traefik)
3. **Set strong CORS origins** in production
4. **Use .env file** securely (never commit to git)
5. **Regular updates** of Docker images and dependencies

### Example Production Setup

```bash
# Use production environment file
cp .env.docker.example .env.production
nano .env.production

# Start with production config
docker-compose --env-file .env.production up -d
```

### Reverse Proxy (nginx)

Example nginx configuration for production:

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Backup and Data

### Backup Logs

```bash
# Copy logs from volume
docker cp awies-backend:/app/logs ./backup-logs
```

### Backup Configuration

```bash
# Backup .env file
cp .env .env.backup.$(date +%Y%m%d)
```

## Monitoring

### Resource Usage

```bash
# Real-time stats
docker stats awies-backend awies-frontend

# Disk usage
docker system df
```

### Log Rotation

Logs are stored in Docker volumes. Configure log rotation:

```bash
# Check log size
docker exec awies-backend du -sh /app/logs

# Clear old logs (if needed)
docker exec awies-backend find /app/logs -name "*.log" -mtime +30 -delete
```

## Uninstallation

```bash
# Stop and remove all containers, networks, volumes
docker-compose down -v

# Remove images
docker rmi awies-backend awies-frontend

# Clean up unused resources
docker system prune -a
```

## Getting Help

- Check logs: `docker-compose logs -f`
- Test API: http://localhost:8000/docs
- Verify health: `curl http://localhost:8000/api/health`
- GitHub Issues: https://github.com/your-repo/issues

## FAQ

**Q: Can I use multiple LLM providers?**
A: Currently only one provider at a time. Switch by changing `.env` and restarting.

**Q: How do I update the application?**
A: `git pull && docker-compose up -d --build`

**Q: What's the minimum hardware requirements?**
A: 2GB RAM, 2 CPU cores, 10GB disk space

**Q: Can I run this on ARM (M1/M2 Mac)?**
A: Yes, Docker will automatically use appropriate base images.

**Q: How secure is storing API keys in .env?**
A: Secure for local/development. For production, use Docker secrets or cloud secret managers.
