run:
	@poetry run python manage.py runserver
migrate:
	@poetry run python manage.py makemigrations --noinput
	@poetry run python manage.py migrate
apply_migrate:
	@poetry run python manage.py migrate
start_seed:
	@poetry run python manage.py start_seed
lint:
	@poetry run flakehell lint
files:
	@poetry run python manage.py collectstatic --noinput
start:
	make apply_migrate
	make files
	make start_seed
