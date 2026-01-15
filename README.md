# Payout Service

REST API для управления заявками на выплату средств.

## Технологии

- Python 3.11
- Django 4.2 + DRF
- Celery + Redis
- PostgreSQL
- Docker

## Быстрый старт

```bash
docker-compose up --build
API: http://localhost:8000/api/payouts/

Swagger: http://localhost:8000/api/docs/

API Endpoints
етодURLписание
GET/api/payouts/Список заявок
POST/api/payouts/Создать заявку
GET/api/payouts/{id}/олучить заявку
PATCH/api/payouts/{id}/бновить заявку
DELETE/api/payouts/{id}/Удалить заявку
POST/api/payouts/{id}/cancel/тменить заявку
Тестирование
Bash

docker-compose exec web pytest
Production Deployment
еобходимые сервисы
PostgreSQL - основная база данных
Redis - брокер Celery
Nginx - reverse proxy
Gunicorn - WSGI сервер
Celery Worker - обработка задач
еплой на VPS
Bash

# Установить Docker
curl -fsSL https://get.docker.com | sh

# Клонировать проект
git clone https://github.com/YOUR_USERNAME/payout-service.git
cd payout-service

# Настроить .env
cp .env.example .env
nano .env  # зменить SECRET_KEY

# Запустить
docker-compose up -d
собенности
UUID идентификаторы
Atomic transactions
select_for_update (race conditions)
Celery retry с backoff
State machine для статусов
