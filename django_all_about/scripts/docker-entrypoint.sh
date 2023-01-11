#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

POSTGRES_HOST=${POSTGRES_HOST:-"postgres"}
POSTGRES_PORT=${POSTGRES_PORT:-"5432"}
REDIS_HOST=${REDIS_HOST:-"redis"}
REDIS_PORT=${REDIS_PORT:-"6379"}

dockerize -wait tcp://${POSTGRES_HOST}:${POSTGRES_PORT} -timeout 100s -wait-retry-interval 5s
dockerize -wait tcp://${REDIS_HOST}:${REDIS_PORT} -timeout 100s -wait-retry-interval 5s

exec "$@"
