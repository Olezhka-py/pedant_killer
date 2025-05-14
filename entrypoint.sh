set -e

poetry run alembic upgrade head
poetry run bot