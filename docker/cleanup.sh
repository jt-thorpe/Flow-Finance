#!/bin/bash

echo "Removing all stopped containers..."
docker rm $(docker ps -aq)

echo "Removing unused Docker images..."
docker rmi $(docker images -q) --force

echo "Removing unused Docker volumes..."
docker volume prune -f

echo "Cleanup complete!"
