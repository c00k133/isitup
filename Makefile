DOCKER_COMPOSE_DEV = docker-compose.dev.yml

.PHONY: run-dev
run-dev: $(DOCKER_COMPOSE_DEV)
	docker-compose --file $^ up

.PHONY: peek-data
peek-data: $(DOCKER_COMPOSE_DEV)
	docker-compose --file $^ exec -u postgres postgres psql --dbname=postgres --command="SELECT * FROM pings;"

.PHONY: rebuild-dev
build-dev: $(DOCKER_COMPOSE_DEV)
	docker-compose --file $^ up --detach --build isitup-consumer-dev isitup-producer-dev


DOCKER_COMPOSE_PROD = docker-compose.prod.yml

.PHONY: run-prod
run-prod: $(DOCKER_COMPOSE_PROD)
	docker-compose --file $^ up
