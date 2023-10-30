#!/bin/bash

exec docker run --name sthali-crud --rm -p 9000:80 sthali-crud

set -e

if [ "$ENV" = 'DOCKER' ]; then
    echo "Running docker"
    exec docker run --name sthali-crud --rm -p 9000:80 sthali-crud
elif [ "$ENV" = 'LOCAL' ]; then
    echo "Running local"
    exec cd src && uvicorn src.run:app --host 0.0.0.0 --port 9000
else
    echo "No ENV found, nothing to run!!!"
fi
