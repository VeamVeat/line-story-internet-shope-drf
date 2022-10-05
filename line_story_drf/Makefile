NAME_CONTAINER += "web"

## build: Build dev python image.
build:
	sudo docker-compose -f docker-compose.yml build $(c)

## build-prod: Build dev prod python image.
build-prod:
	sudo docker-compose -f docker-compose-prod.yml build $(c)

## build-alpine: Build dev alpine python image.
build-alpine:
	sudo docker-compose -f docker-compose-alpine.yml build $(c)

## build-prod-alpine: Build prod alpine python image.
build-prod-alpine:
	sudo docker-compose -f docker-compose-prod-alpine.yml build $(c)

## up: Start dev up containers.
up:
	sudo docker-compose -f docker-compose.yml up $(c)

## up-prod: Start prod up containers.
up-prod:
	sudo docker-compose -f docker-compose-prod.yml up $(c)

## up-alpine: Start dev alpine up containers.
up-alpine:
	sudo docker-compose -f docker-compose-alpine.yml up $(c)

## up-prod-alpine: Start prod alpine up containers.
up-prod-alpine:
	sudo docker-compose -f docker-compose-prod-alpine.yml up $(c)

## start: Start dev alpine containers.
start:
	sudo docker-compose -f docker-compose.yml start $(c)

## down: destroy dev containers.
down:
	sudo docker-compose -f docker-compose.yml down -v $(c)

## down-alpine: destroy dev alpine containers.
down-alpine:
	sudo docker-compose -f docker-compose-alpine.yml down -v $(c)

## down-prod: destroy prod containers.
down-prod:
	sudo docker-compose -f docker-compose-prod.yml down -v $(c)

## down-prod-alpine: destroy prod alpine containers.
down-prod-alpine:
	sudo docker-compose -f docker-compose-prod-alpine.yml down -v $(c)

## stop: stop dev containers.
stop:
	sudo docker-compose -f docker-compose.yml stop $(c)

## restart: restart dev containers.
restart:
	sudo docker-compose -f docker-compose.yml stop $(c)
	sudo docker-compose -f docker-compose.yml up -d $(c)

## logs: get logs dev containers.
logs:
	sudo docker-compose -f docker-compose.yml logs --tail=100 -f $(c)

## ps: see running dev containers.
ps:
	sudo docker-compose -f docker-compose.yml ps

## login-api: enter the dev container web
login:
	sudo docker-compose -f docker-compose.yml exec $(NAME_CONTAINER) bash

## login-prod-web: enter the prod container web
login-prod:
	sudo docker-compose -f docker-compose.prod.yml exec $(NAME_CONTAINER) bash

## login-alpine-web: enter the alpine dev container web
login-alpine:
	sudo docker-compose -f docker-compose-alpine.yml exec $(NAME_CONTAINER) /bin/sh

## login-prod-alpine-web: enter the alpine prod container web
login-prod-alpine:
	sudo docker-compose -f docker-compose-alpine.yml exec $(NAME_CONTAINER) /bin/sh

db-shell:
	sudo docker-compose -f docker-compose.yml exec timescale psql -Upostgres

## prune-all: clear all data container all
prune-all:
	sudo sudo docker system prune

## prune-volume: clear all data volume all
prune-volume:
	sudo sudo docker volume prune

## prune-image: clear all data image all
prune-image:
	sudo docker image prune

## prune-container: clear all data container all
prune-container:
	sudo docker container prune

create-superuser:
	python manage.py createsuperuser

migrate:
	python manage.py migrate
