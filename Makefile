.PHONY: all
all: infra app

# Common variables
DC=docker compose
APP_NAME=django-aiogram-template

# App
APP-DC=$(DC) -f ./docker/app.compose.yaml -p $(APP_NAME)

.PHONY: app
app:
	@$(APP-DC) down
	@$(APP-DC) up --build

.PHONY: django-shell
django-shell:
	@$(APP-DC) exec backend uv run /app/manage.py shell

.PHONY: create-admin
create-admin:
	@$(APP-DC) exec backend uv run /app/manage.py createsuperuser


# Infra
INFRA-DC=$(DC) -f ./docker/infra.compose.yaml -p $(APP_NAME) --env-file .env

.PHONY: infra
infra:
	@$(INFRA-DC) down
	@$(INFRA-DC) up -d

infra-down:
	@$(INFRA-DC) down