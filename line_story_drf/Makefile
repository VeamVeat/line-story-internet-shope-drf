NAME_CONTAINER += 'web'

DC += docker-compose -f
MIGRATE += python manage.py migrate --noinput

DC_NAME += 'docker-compose.yml'
DC_ALPINE_NAME += 'docker-compose-alpine.yml'
DC_PROD_NAME += 'docker-compose-prod.yml'
DC_PROD_ALPINE_NAME += 'docker-compose-prod-alpine.yml'

## build: Build dev python image.
build:
	$(DC) $(DC_NAME) build

## build-prod: Build dev prod python image.
build-prod:
	$(DC) $(DC_PROD_NAME) build

## build-alpine: Build dev alpine python image.
build-alpine:
	$(DC) $(DC_ALPINE_NAME) build

## build-prod-alpine: Build prod alpine python image.
build-prod-alpine:
	$(DC) $(DC_PROD_ALPINE_NAME) build

## up: Start dev up containers.
up:
	$(DC) $(DC_NAME) up

## up-prod: Start prod up containers.
up-prod:
	$(DC) $(DC_PROD_NAME) up

## up-alpine: Start dev alpine up containers.
up-alpine:
	$(DC) $(DC_ALPINE_NAME) up

## up-prod-alpine: Start prod alpine up containers.
up-prod-alpine:
	$(DC) $(DC_PROD_ALPINE_NAME) up

## start: Start dev alpine containers.
start:
	$(DC) $(DC_NAME) start

## down: destroy dev containers.
down:
	$(DC) $(DC_NAME) down -v

## down-alpine: destroy dev alpine containers.
down-alpine:
	$(DC) $(DC_ALPINE_NAME) down -v

## down-prod: destroy prod containers.
down-prod:
	$(DC) $(DC_PROD_NAME) down -v

## down-prod-alpine: destroy prod alpine containers.
down-prod-alpine:
	$(DC) $(DC_PROD_ALPINE_NAME) down -v

## stop: stop dev containers.
stop:
	$(DC) $(DC_NAME) stop

## restart: restart dev containers.
restart:
	$(DC) $(DC_NAME) stop
	$(DC) $(DC_NAME) up -d

## logs: get logs dev containers.
logs:
	$(DC) $(DC_NAME) logs --tail=100 -f

## ps: see running dev containers.
ps:
	$(DC) $(DC_NAME) ps

## login-api: enter the dev container web
login:
	$(DC) $(DC_NAME) exec $(NAME_CONTAINER) bash

## login-prod-web: enter the prod container web
login-prod:
	$(DC) $(DC_PROD_NAME) exec $(NAME_CONTAINER) bash

## login-alpine-web: enter the alpine dev container web
login-alpine:
	$(DC) $(DC_ALPINE_NAME) exec $(NAME_CONTAINER) /bin/sh

## login-prod-alpine-web: enter the alpine prod container web
login-prod-alpine:
	$(DC) $(DC_PROD_ALPINE_NAME) exec $(NAME_CONTAINER) /bin/sh

db-shell:
	$(DC) $(DC_NAME) exec timescale psql -Upostgres

## prune-all: clear all data container all
prune-all:
	docker system prune

## prune-volume: clear all data volume all
prune-volume:
	docker volume prune

## prune-image: clear all data image all
prune-image:
	docker image prune

## prune-container: clear all data container all
prune-container:
	docker container prune

create-superuser:
	python manage.py createsuperuser

migrate-prod:
	$(DC) $(DC_NAME) exec $(NAME_CONTAINER) $(MIGRATE)

migrate-prod-alpine:
	$(DC) $(DC_ALPINE_NAME) exec $(NAME_CONTAINER) $(MIGRATE)
