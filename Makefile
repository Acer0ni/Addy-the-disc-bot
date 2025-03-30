.PHONY: *

up:
	docker compose up bot

run:
	docker compose run --rm bot $(filter-out $@,$(MAKECMDGOALS))

build:
	docker compose build

migrations:
	docker compose run --rm bot uv run alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"

migrate:
	docker compose run --rm bot uv run alembic upgrade head

uv:
	docker compose run -it --rm bot uv $(filter-out $@,$(MAKECMDGOALS))  
seed:
	docker compose run -it --rm bot uv run seed.py