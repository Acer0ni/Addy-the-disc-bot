FROM python:3.10-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app/
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --link-mode copy 
COPY bot.py  alembic.ini  seed.py ./
COPY addy ./addy/
COPY alembic ./alembic/
COPY data ./data/
CMD uv run bot.py


