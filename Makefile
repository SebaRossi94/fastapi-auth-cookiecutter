runserver:
	poetry run uvicorn app.main:app --reload

dbinit:
	poetry run alembic init ./migrations

createmigration:
	poetry run alembic revision --autogenerate -m 'init'

dbupgrade:
	poetry run alembic upgrade head

dbdowngrade:
	poetry run alembic downgrade head