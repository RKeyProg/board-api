@a_default:
  just --list

@dev:
  uv run uvicorn app.main:app --reload --log-config log_conf.yaml

@prod:
  uv run uvicorn app.main:app --log-config log_conf.prod.yaml

@lint:
  uv run ruff check --fix

@format:
  uv run ruff format