# Restaurant API

FastAPI project for managing a restaurant

|VERSION            |DESCRIPTION                       |
|-------------------|----------------------------------|
|Python             |3.11                              |
|Poetry             |1.4.2                             |
|Postgres           |14.7                              |

## Setup

1. Define environment varaibles by creating a .env file based on .env.example
```
cp .env.example .env
```
|VARIABLE            |DESCRIPTION                                            |
|--------------------|-------------------------------------------------------|
|APP_NAME            |Name of the app                                        |
|APPLICATION_VERSION |Last version of the application                        |
|APP_ENVIRONMENT     |Name of the application environment                    |
|DEBUG               |Debug flag                                             |
|LOG_LEVEL           |Defines the level of the logs that are shown in console|
|SECRET_KEY          |Defines secret key for some features of the application|
|DB_HOST             |Database host                                          |
|DB_PORT             |Database port                                          |
|DB_USER             |Database user                                          |
|DB_PASSWORD         |Database password                                      |
|DB_NAME             |Database name                                          |

## Run using docker-compose
```
docker-compose -f ./compose/develop/docker-compose.yml up --build
```

## Run using poetry
```
poetry install
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