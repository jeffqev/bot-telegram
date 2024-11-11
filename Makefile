LOCAL_DOCKER_COMPOSE = ./infrastructure/local/docker-compose.yml

up:
	docker-compose -f $(LOCAL_DOCKER_COMPOSE) up -d

down:
	docker-compose -f $(LOCAL_DOCKER_COMPOSE) down

logs:
	docker-compose -f $(LOCAL_DOCKER_COMPOSE) logs -f ai-api bot

shell-ai:
	docker-compose -f $(LOCAL_DOCKER_COMPOSE) run --no-deps --rm ai-api zsh

shell-bot:
	docker-compose -f $(LOCAL_DOCKER_COMPOSE) run --no-deps --rm bot zsh

rebuild-ai:
	docker-compose -f $(LOCAL_DOCKER_COMPOSE) up -d --build ai-api

rebuild-bot:
	docker-compose -f $(LOCAL_DOCKER_COMPOSE) up -d --build bot

test-ai:
	docker-compose -f $(LOCAL_DOCKER_COMPOSE) run --no-deps --rm ai-api pytest

test: test-bot test-ai

test-bot:
	docker-compose -f $(LOCAL_DOCKER_COMPOSE) run --no-deps --rm bot npm run test


clean:
	docker-compose -f $(LOCAL_DOCKER_COMPOSE) down -v --rmi local --remove-orphans