FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl build-essential \
 && pip install pipx \
 && pipx install poetry \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pipx run poetry install --no-root

COPY . .

CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run bot"]