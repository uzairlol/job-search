# job-search

A modular, extensible autonomous job acquisition platform.

## Phase 1

This first phase establishes:
- a modular Python application layout
- typed domain models
- a health endpoint
- a sample company discovery service
- initial tests

## Development

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
uvicorn app.main:app --reload
```
