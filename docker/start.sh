#!/bin/bash

echo "Stopping existing containers..."
docker compose down --volumes

echo "Building and starting containers..."
docker compose up --build -d

echo "Containers are up and running!"
