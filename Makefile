runserver:
	poetry run uvicorn app.main:app --reload

dbinit:
	poetry run alembic init ./migrations

runflake:
	poetry run flake8 app

runblack:
	poetry run black app

build:
	DOCKER_ENV=dev docker compose build --no-cache
	
test:
	DOCKER_ENV=test docker compose run --rm fastapi_auth_app pytest "$(path)"

run:
	DOCKER_ENV=dev docker compose up

stop:
	DOCKER_ENV=dev docker compose stop

rundeamon:
	DOCKER_ENV=dev docker compose up -d

dbupgrade:
	DOCKER_ENV=dev docker compose run fastapi_auth_app alembic upgrade head

dbdowngrade:
	DOCKER_ENV=dev docker compose run fastapi_auth_app alembic downgrade head

createmigration:
	DOCKER_ENV=dev docker compose run fastapi_auth_app alembic revision --autogenerate -m "$(message)"