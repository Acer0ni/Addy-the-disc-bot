FROM python:3.10-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app/
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --link-mode copy 
COPY bot.py addy/ alembic/ alembic.ini data/ seed.py ./
CMD uv run bot.py


