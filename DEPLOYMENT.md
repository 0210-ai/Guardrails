# Deployment Guide

## Prerequisites

- Python 3.9+
- Node.js 18+
- Docker & Docker Compose (for container deployment)
- GitHub App credentials
- Google Gemini API key (optional, for AI features)

## Environment Variables

### Backend
```bash
# Required
GOOGLE_API_KEY=<your-gemini-api-key>  # Optional for AI suggestions

# Optional
DEBUG=false
HOST=0.0.0.0
PORT=8000
```

### GitHub App
```bash
# Required
BACKEND_URL=<your-backend-url>
APP_ID=<github-app-id>
PRIVATE_KEY=<github-app-private-key>
WEBHOOK_SECRET=<github-webhook-secret>
```

## Local Development

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend runs on `http://localhost:8000`

### 2. GitHub App Setup

```bash
cd guardrails-github-app
npm install
npm run build
npm start
```

App runs on `http://localhost:3000`

## Docker Deployment

### Using Docker Compose

1. **Create `.env` file in root directory:**

```bash
# Backend
GOOGLE_API_KEY=your-gemini-api-key
DEBUG=false

# GitHub App
BACKEND_URL=http://backend:8000
APP_ID=your-github-app-id
PRIVATE_KEY=your-github-app-private-key
WEBHOOK_SECRET=your-webhook-secret
```

2. **Start services:**

```bash
docker-compose up -d
```

Services:
- Backend API: http://localhost:8000
- GitHub App: http://localhost:3000

3. **View logs:**

```bash
docker-compose logs -f
```

4. **Stop services:**

```bash
docker-compose down
```

### Docker Compose Configuration

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - DEBUG=${DEBUG}
      - HOST=0.0.0.0
      - PORT=8000
    volumes:
      - ./backend/audit_logs:/app/audit_logs
    restart: always

  github-app:
    build: ./guardrails-github-app
    ports:
      - "3000:3000"
    environment:
      - BACKEND_URL=${BACKEND_URL}
      - APP_ID=${APP_ID}
      - PRIVATE_KEY=${PRIVATE_KEY}
      - WEBHOOK_SECRET=${WEBHOOK_SECRET}
    depends_on:
      - backend
    restart: always
```

## Normal Deployment (Without Docker)

### 1. Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_API_KEY="your-gemini-api-key"
export DEBUG="false"

# Run with uvicorn
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 2. GitHub App

```bash
cd guardrails-github-app

# Install dependencies
npm install

# Build
npm run build

# Set environment variables
export BACKEND_URL="http://localhost:8000"
export APP_ID="your-github-app-id"
export PRIVATE_KEY="your-private-key"
export WEBHOOK_SECRET="your-webhook-secret"

# Run
npm start
```

## Health Checks

### Backend Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "ai_enabled": true,
  "timestamp": "2026-01-28T10:00:00"
}
```

### GitHub App Health Check

```bash
curl http://localhost:3000/
```

## Security

- Keep API keys in environment variables (never commit to git)
- Use strong webhook secrets
- Enable HTTPS in production
- Restrict network access to internal services
- Regularly rotate GitHub App credentials

## Troubleshooting

### Backend won't start
- Check `GOOGLE_API_KEY` is set correctly
- Verify port 8000 is not in use
- Check logs: `docker-compose logs backend`

### GitHub App connection issues
- Verify `BACKEND_URL` is correct
- Check GitHub App credentials are valid
- Ensure backend is running

### AI suggestions not working
- Verify `GOOGLE_API_KEY` environment variable is set
- Check Gemini API quota and permissions
- Enable debug mode: `DEBUG=true`

### Port conflicts
- Change port in docker-compose.yml or uvicorn command
- Example: `--port 8001` for alternative port
