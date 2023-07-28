# Fast API Template

FastAPI blank template created to start any new project

## Setup

1. Define environment varaibles by creating a .env file based on .env.example
```
cp .env.example .env
```

## Run using docker-compose
```
#Option 1
docker-compose -f ./compose/develop/docker-compose.yml up --build

#Option 2
. ./scripts/start-docker-dev.sh
```

## Run using poetry
```
poetry install
```
```
poetry run sh ./scripts/start-dev.sh
```

## Run migrations
```
# Option 1
. ./scripts/migrate.sh

# Option 2
alembic revision --autogenerate -m "migration $(date +"%Y-%m-%d %H:%M:%S")"
alembic upgrade head
```