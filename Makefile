python := myvenv/Scripts/python.exe -u

compose := docker compose -f docker-compose.local.yml


python:
	$(python)

container-build:
	$(compose) build

container-down:
	$(compose) down --remove-orphans -t 0

daemon:
	$(compose) up -d

crawl:
	$(python) manage.py crawl

super-user:
	$(python) manage.py  createsuperuser

system-clean:
	bash bash/docker-clean.sh

logs:
	$(compose) logs -f

logs-django:
	$(compose) logs -f django nginx postgres celeryworker

delete:
	sudo rm -r ./data ./staticfiles ./dist

locale-create:
	$(python) manage.py makemessages --all

locale-save:
	$(python) manage.py compilemessages

celery:
	$(python) -m  celery -A config.celery_app worker -l INFO --pool solo

start:
	$(python) manage.py runserver

server:
	$(python) -m gunicorn --config gunicorn-cfg.py config.wsgi 

migrate:
	$(python) manage.py migrate

migrations:
	$(python) manage.py makemigrations

static:
	$(python) manage.py collectstatic --noinput

dev:
	npm run dev

build:
	npm run build

clean:
	npm run clean

format:
	$(python) -m djlint rhixe_scans/templates/**/*.html --reformat

format-check:
	$(python) -m djlint rhixe_scans/templates/**/*.html --check
