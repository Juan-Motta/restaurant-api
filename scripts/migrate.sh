#!/bin/bash

alembic revision --autogenerate -m "migration $(date +"%Y-%m-%d %H:%M:%S")"

alembic upgrade head
