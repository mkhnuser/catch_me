docker system prune --all --force
docker compose -f docker-compose.yaml -f docker-compose.production.yaml up
