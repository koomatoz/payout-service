.PHONY: help up down logs test

help:
	@echo "make up      - Start all services"
	@echo "make down    - Stop all services"
	@echo "make logs    - View logs"
	@echo "make test    - Run tests"
	@echo "make migrate - Run migrations"

up:
	docker-compose up --build

down:
	docker-compose down

logs:
	docker-compose logs -f

test:
	docker-compose exec web pytest

migrate:
	docker-compose exec web python src/manage.py migrate

migrations:
	docker-compose exec web python src/manage.py makemigrations