.PHONY: up down restart db-init db-seed test lint

up:
	docker compose -f deploy/docker-compose.yml up -d postgres redis

down:
	docker compose -f deploy/docker-compose.yml down

restart: down up

db-init:
	@export PGPASSWORD='Admin@90088*'; \
	docker compose -f deploy/docker-compose.yml up -d postgres; \
	sleep 3; \
	psql -h localhost -U postgres -d ai_crm -f database/schemas/001-init.sql 2>/dev/null || true; \
	psql -h localhost -U postgres -d ai_crm -f database/schemas/002-crm-core.sql; \
	psql -h localhost -U postgres -d ai_crm -f database/schemas/003-ai-modules.sql; \
	psql -h localhost -U postgres -d ai_crm -f database/schemas/004-business-modules.sql; \
	psql -h localhost -U postgres -d ai_crm -f database/schemas/005-auth.sql; \
	psql -h localhost -U postgres -d ai_crm -f database/schemas/006-system.sql; \
	psql -h localhost -U postgres -d ai_crm -f database/schemas/007-knowledge.sql

db-seed:
	@export PGPASSWORD='Admin@90088*'; \
	psql -h localhost -U postgres -d ai_crm -f database/seed_data.sql

api:
	cd backend && source venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	cd backend && source venv/bin/activate && python -m pytest tests/ -v --cov=app --cov-report=term

lint:
	cd backend && source venv/bin/activate && ruff check app/ tests/ 2>/dev/null || flake8 app/ tests/ --max-line-length=120 2>/dev/null || echo "Install ruff: pip install ruff"
