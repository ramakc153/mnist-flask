FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

RUN uv pip install -r pyproject.toml

CMD ["uv","run", "app/main.py"]