FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim



WORKDIR /app

COPY . .

RUN uv pip install -r pyproject.toml
EXPOSE 5000

CMD ["uv","run", "app/main.py"]
