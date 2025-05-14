FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl build-essential \
    && pip install pipx \
    && pipx install poetry \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /pedant_killer

COPY pyproject.toml poetry.lock* ./
COPY README.md ./

RUN poetry install --no-root

COPY . .

RUN poetry install

CMD poetry run alembic upgrade head && poetry run bot