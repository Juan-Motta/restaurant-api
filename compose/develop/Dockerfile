FROM python:3.11-slim AS build

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt update \
    && apt install -y curl \
    && pip install --upgrade pip \
    && pip install poetry

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry export -f --dev requirements.txt --output /app/requirements.txt --without-hashes

RUN pip install -r requirements.txt

COPY  . .

RUN sed -i 's/\r//g' ./scripts/*.sh
RUN chmod +x ./scripts/*.sh

CMD ["./scripts/start-dev.sh"]