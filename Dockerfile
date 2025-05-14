FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl build-essential \
    && pip install pipx \
    && pipx install poetry \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH="/pedant_killer:$PYTHONPATH"
ENV PYTHONUNBUFFERED=1


WORKDIR /pedant_killer

COPY pyproject.toml poetry.lock* ./
COPY README.md ./


RUN poetry install --no-root
RUN poetry config virtualenvs.create false

COPY . .

RUN poetry install

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]