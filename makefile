PROJECT_NAME = my_django_project
PYTHON = python3
MANAGE = $(PYTHON) manage.py

venv:
	$(PYTHON) -m venv venv
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

run:
	$(MANAGE) runserver

migrate:
	$(MANAGE) migrate

makemigrations:
	$(MANAGE) makemigrations

test:
	$(MANAGE) test

superuser:
	$(MANAGE) createsuperuser

collectstatic:
	$(MANAGE) collectstatic --noinput

lint:
	flake8 .

format:
	black .

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

install:
	pip install -r requirements.txt

shell:
	$(MANAGE) shell

newapp:
	$(MANAGE) startapp $(APP_NAME)

help:
	@echo "Available commands:"
	@echo "  make venv"
	@echo "  make run"
	@echo "  make migrate"
	@echo "  make makemigrations"
	@echo "  make test"
	@echo "  make superuser"
	@echo "  make collectstatic"
	@echo "  make lint"
	@echo "  make format"
	@echo "  make clean"
	@echo "  make install"
	@echo "  make shell"
	@echo "  make newapp APP_NAME=<app_name>"
