THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help build up start down destroy stop restart logs logs-api ps login-timesc


down:
	docker-compose -f docker-compose.dev.yaml down

run:
	docker-compose -f docker-compose.dev.yaml up -d --build

migrations:
	docker exec -it order-service alembic upgrade head