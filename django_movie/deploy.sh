#!/bin/bash

# Django Movie App Deployment Script
# This script handles deployment and optimization tasks

set -e

echo "🚀 Starting Django Movie App Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install requirements
print_status "Installing requirements..."
pip install -r requirements.txt

# Create logs directory
print_status "Creating logs directory..."
mkdir -p logs

# Environment setup
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Copying from .env.example..."
    cp .env.example .env
    print_warning "Please update .env file with your configuration!"
fi

# Database migrations
print_status "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (optional)
read -p "Do you want to create a superuser? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Database optimization
print_status "Optimizing database..."
python manage.py optimize_db --clear-cache --analyze-tables

# Test the application
print_status "Running tests..."
python manage.py test --verbosity=2

print_status "✅ Deployment completed successfully!"
print_status "🔧 To start the development server: python manage.py runserver"
print_status "🔧 To start Celery worker: celery -A django_movie worker -l info"
print_status "🔧 To start Celery beat: celery -A django_movie beat -l info"

echo ""
print_warning "📋 Post-deployment checklist:"
echo "   1. Update .env file with production values"
echo "   2. Configure Redis server"
echo "   3. Set up SSL certificates"
echo "   4. Configure web server (Nginx/Apache)"
echo "   5. Set up monitoring and logging"
echo "   6. Configure backup strategy"