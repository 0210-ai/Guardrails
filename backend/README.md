# Guardrails Backend

Enterprise-grade code guardrails for GitHub Copilot using FastAPI.

## Setup

```bash
pip install -r requirements.txt
```

## Running the Backend

```bash
python main.py
```

Server will run on `http://localhost:8000`

## API Endpoints

- **GET `/health`** - Health check
- **POST `/api/analyze`** - Analyze code diff for violations
- **GET `/api/rules`** - Get list of available security rules

## Example Request

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "repo_name": "owner/repo",
    "pr_number": 123,
    "commit_hash": "abc123def456",
    "files": {
      "src/app.py": "--- a/src/app.py\n+++ b/src/app.py\n@@ -1,3 +1,5 @@\n password = \"secret123\"\n"
    }
  }'
```

## Architecture

- `app/models/` - Data models for violations and scan results
- `app/rules/` - Security rules engine
- `app/analyzers/` - Code analysis logic
- `app/config/` - Configuration management
- `app/main.py` - FastAPI application

## Security Rules

- **SEC-001** - Hardcoded Secrets (API keys, passwords, tokens)
- **SEC-002** - SQL Injection patterns
- **SEC-003** - Insecure Deserialization
- **SEC-004** - Unsafe Code Execution (eval, exec)
- **SEC-005** - Weak Cryptography
