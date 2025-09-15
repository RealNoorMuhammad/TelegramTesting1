@echo off
REM PolyFocus Bot Deployment Script for Windows
REM This script helps deploy the bot to a production environment

echo 🚀 PolyFocus Bot Deployment Script
echo ==================================

REM Check if .env file exists
if not exist .env (
    echo ❌ .env file not found. Please create one from .env.example
    pause
    exit /b 1
)

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Create necessary directories
echo 📁 Creating directories...
if not exist data mkdir data
if not exist logs mkdir logs

REM Build Docker image
echo 🔨 Building Docker image...
docker-compose build

REM Start services
echo 🚀 Starting services...
docker-compose up -d

REM Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Check if bot is running
docker-compose ps | findstr "Up" >nul
if errorlevel 1 (
    echo ❌ Bot failed to start. Check logs:
    docker-compose logs polymarket-bot
    pause
    exit /b 1
) else (
    echo ✅ Bot is running successfully!
    echo.
    echo 📊 Service Status:
    docker-compose ps
    echo.
    echo 📝 View logs with: docker-compose logs -f polymarket-bot
    echo 🛑 Stop with: docker-compose down
)

echo.
echo 🎉 Deployment completed successfully!
echo Your PolyFocus Bot is now running and ready to trade!
pause
