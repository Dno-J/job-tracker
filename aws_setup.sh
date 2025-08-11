#!/bin/bash

# Exit immediately if a command fails
set -e

echo "🔧 Updating system..."
sudo apt update && sudo apt upgrade -y

echo "🐳 Installing Docker..."
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

echo "👤 Adding user to Docker group..."
sudo usermod -aG docker $USER

echo "📁 Cloning your Job Tracker repo..."
git clone https://github.com/Dno-J/job-tracker.git
cd job-tracker

echo "🔐 Loading environment variables..."
cp .env.ec2 .env

echo "🐳 Building and running Docker container..."
docker build -t job-tracker-app .
docker run -d -p 8000:8000 --env-file .env job-tracker-app

echo "✅ Deployment complete. Your FastAPI app is live on port 8000."
