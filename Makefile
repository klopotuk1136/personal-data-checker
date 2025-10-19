build:
	docker build -t personal-data-checker:latest .

up:
	docker compose --env-file .env up -d

rebuild:
	docker build -t personal-data-checker:latest .
	docker compose up -d --force-recreate

down:
	docker compose down