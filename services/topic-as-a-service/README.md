# Topic as a Service (FastAPI)

## Run locally (without Docker)
```bash
python -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
export KAFKA_BOOTSTRAP_SERVERS=localhost:9092
uvicorn app.main:app --host 0.0.0.0 --port 8088 --reload
```

## Auth
Set:
- `AUTH_MODE=api_key`
- `API_KEY=...`
Then call with header `X-API-Key: ...`

## Governance
- `GOVERNANCE_TOPIC_NAME_REGEX`
- `GOVERNANCE_REQUIRE_LABELS` (CSV)
