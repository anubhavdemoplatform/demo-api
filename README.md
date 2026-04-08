# demo-api

Demo FastAPI application — consumer of
[ci-platform](https://github.com/anubhavdemoplatform/ci-platform) governance workflows.

## Local Development

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Tests

```bash
pip install httpx pytest
pytest tests/
```

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/items` | List all items |
| GET | `/items/{id}` | Get item by ID |
| POST | `/items` | Create item |
| DELETE | `/items/{id}` | Delete item |

## Governance

This repo uses the `ci-platform` reusable workflows via `.github/workflows/governance.yml`.
Configuration is in `.github/ai-review-config.yml`.
