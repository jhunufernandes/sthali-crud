#!/bin/bash

set -e

if [ "$ENV" = 'DOCKER' ]; then
    echo "Running docker"
    exec docker run --name sthali-crud --rm -p 9000:80 sthali-crud
elif [ "$ENV" = 'LOCAL' ]; then
    echo "Running local"
    cd ./src/
    exec uvicorn run:app --host 0.0.0.0 --port 9000 --reload
else
    echo "No ENV found, nothing to run!!!"
fi
