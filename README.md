# Restaurant Order Management System

![Python version](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)
[![Continuous integration](https://img.shields.io/github/actions/workflow/status/Juan-Motta/restaurant-api/ci.yml?branch=main&style=flat-square)](https://github.com/Juan-Motta/restaurant-api/actions?query=branch:main)
[![Coverage Status](https://img.shields.io/coverallsCoverage/github/Juan-Motta/restaurant-api?branch=main&style=flat-square)](https://coveralls.io/github/Juan-Motta/restaurant-api)

## Description

This API serves as the backend for a restaurant order management system, built with FastAPI and following hexagonal architecture patterns for clean separation of concerns and adaptability. This backend service is responsible for handling order processing, reporting, bulk customer uploads, and authentication.

### Data Model

![image](https://github.com/user-attachments/assets/2504e379-cc01-48a8-8f3c-005471f018c5)

## Technical Stack

- FastAPI: Web framework for building APIs with Python.
- PostgreSQL: Robust and powerful SQL database for storing and querying data.
- Redis: In-memory data store used as cache and message broker.
- Celery: Asynchronous task queue/job queue based on distributed message passing.
- MQTT: For real-time notifications to clients.
- Docker and Docker-Compose: For containerization and local deployment of the service.

## Project Structure

Following hexagonal architecture guidelines, our project is divided into:

- **Application**: The driving side of the application that contains service definitions. 
- **Domain**: Core logic and business rules of the application.
- **Infrastructure**: Communication with external agents such as databases, APIs, etc.

## Features

- Authentication using JWT tokens.
- Bulk upload of customer details via CSV/XLSX.
- Generation and handling of reports in CSV format.
- Asynchronous task management for file uploads/downloads and notification delivery.
- Granular permission control and secure handling of sensitive data.

## Endpoints

- User authentication and token creation.
- Order status management.
- Real-time order status updates through MQTT.
- Bulk customer creation from a CSV/XLSX route, limited to 20 entries per upload.
- Metrics dashboard endpoint exposing popular statistics per restaurant.

## Tasks monitoring
To monitor asynchronous tasks using Celery, there is a dashboard implemented using Celery Insights.

![image](https://github.com/user-attachments/assets/53291e7f-bb0d-4640-bbc4-db65c0f910c3)


## Getting Started

### Prerequisites

**Containerized**
- Docker
- Docker-Compose
  
**Local**
- UV
- Postgresql
- Redis

### Installation with docker

1. Clone the repository:
   ```sh
   git clone https://github.com/Juan-Motta/restaurant-api.git
   ```
2. Navigate to the project directory:
   ```
   cd path/to/restaurant-api
   ```
3. Create .env file and populate it with the following data:
   ```
    # path/to/restaurant-api/.env

    APP_TITLE="Restaurant API"
    APP_VERSION="0.1.0"`

    DEBUG="True"

    # Docker
    DB_HOST="postgres"
    DB_PORT="5432"
    DB_USER="postgres"
    DB_PASSWORD="postgres"
    DB_NAME="restaurant_db"
    DB_DRIVER="postgresql+psycopg"`

    REDIS_HOST="redis"
    REDIS_PORT="6379"

    JWT_SECRET_KEY="secret"
   ```
   Environment variables are used to manage configurations and secrets, sample structure provided in .env.example.

4. Build and run the containers using Docker:
   ```
   docker-compose up --build
   ```
    The services should now be accessible at
    * API: http://localhost:9000
    * API Docs: http://localhost:9000/docs
    * Celery monitoring: http://localhost:8555.
   
    To change default port modify the file docker-compose.yml.

6. Run the provided script to initialize the database with some test data:
   ```
   docker-compose exec web python scripts/init_db.py
   ```
