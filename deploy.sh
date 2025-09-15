#!/bin/bash

# PolyFocus Bot Deployment Script
# This script helps deploy the bot to a production environment

set -e

echo "🚀 PolyFocus Bot Deployment Script"
echo "=================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create one from .env.example"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data logs

# Set proper permissions
chmod 755 data logs

# Build Docker image
echo "🔨 Building Docker image..."
docker-compose build

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if bot is running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Bot is running successfully!"
    echo ""
    echo "📊 Service Status:"
    docker-compose ps
    echo ""
    echo "📝 View logs with: docker-compose logs -f polymarket-bot"
    echo "🛑 Stop with: docker-compose down"
else
    echo "❌ Bot failed to start. Check logs:"
    docker-compose logs polymarket-bot
    exit 1
fi

echo ""
echo "🎉 Deployment completed successfully!"
echo "Your PolyFocus Bot is now running and ready to trade!"
