#! /usr/bin/env bash

# Create alias for manual using inside docker container
./scripts/alias.sh


# Run migrations
alembic upgrade head
