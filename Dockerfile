FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl build-essential \
    && pip install pipx \
    && pipx install poetry \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root

COPY . .

# Команда для запуска миграций и бота
CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run python bot.py"]