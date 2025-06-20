.PHONY: help build up down logs shell migrate test clean

# Variables
COMPOSE_FILE = docker-compose.yml
APP_CONTAINER = aula-calendar-app
DB_CONTAINER = aula-postgres

help:  ## Afficher cette aide
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build:  ## Construire les images Docker
	docker-compose -f $(COMPOSE_FILE) build

up:  ## D?marrer tous les services
	docker-compose -f $(COMPOSE_FILE) up -d

down:  ## Arr?ter tous les services
	docker-compose -f $(COMPOSE_FILE) down

logs:  ## Voir les logs de l'application
	docker-compose -f $(COMPOSE_FILE) logs -f $(APP_CONTAINER)

logs-all:  ## Voir tous les logs
	docker-compose -f $(COMPOSE_FILE) logs -f

shell:  ## Ouvrir un shell dans le container de l'app
	docker-compose -f $(COMPOSE_FILE) exec $(APP_CONTAINER) /bin/bash

db-shell:  ## Ouvrir un shell PostgreSQL
	docker-compose -f $(COMPOSE_FILE) exec $(DB_CONTAINER) psql -U aula_user -d aula_calendar

test:  ## Ex?cuter les tests
	docker-compose -f $(COMPOSE_FILE) exec $(APP_CONTAINER) python -m pytest tests/ -v

test-cov:  ## Ex?cuter les tests avec couverture
	docker-compose -f $(COMPOSE_FILE) exec $(APP_CONTAINER) python -m pytest tests/ --cov=app --cov-report=html

clean:  ## Nettoyer les containers et volumes
	docker-compose -f $(COMPOSE_FILE) down -v
	docker system prune -f

restart:  ## Red?marrer l'application
	docker-compose -f $(COMPOSE_FILE) restart $(APP_CONTAINER)

backup-db:  ## Sauvegarder la base de donn?es
	docker-compose -f $(COMPOSE_FILE) exec $(DB_CONTAINER) pg_dump -U aula_user aula_calendar > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore-db:  ## Restaurer la base de donn?es (usage: make restore-db FILE=backup.sql)
	docker-compose -f $(COMPOSE_FILE) exec -T $(DB_CONTAINER) psql -U aula_user -d aula_calendar < $(FILE)

# D?veloppement
dev-setup:  ## Configuration pour le d?veloppement
	cp .env.example .env
	@echo "?ditez le fichier .env avec vos param?tres"
	@echo "Puis lancez: make build && make up"

dev:  ## Lancer en mode d?veloppement
	docker-compose -f docker-compose.dev.yml up --build