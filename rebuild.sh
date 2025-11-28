#!/bin/bash
# Script to rebuild Docker container and clean up old images

echo "🛑 Stopping containers..."
docker compose down

echo ""
echo "🗑️  This will remove unused Docker images."
read -p "Do you want to continue? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Removing old images..."
    docker image prune -f
else
    echo "⏭️  Skipping image cleanup..."
fi

echo "🔨 Building new image..."
docker compose build --no-cache

echo "🚀 Starting containers..."
docker compose up -d

echo "⏳ Waiting for health check..."
sleep 3

echo "✅ Checking health..."
curl http://localhost:8000/health

echo ""
echo "✨ Done! Container is running."
