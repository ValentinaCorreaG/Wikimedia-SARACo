#!/bin/bash

# SARA Setup Script
# This script helps you set up the SARA project quickly

set -e  # Exit on error

echo "🚀 SARA Setup Script"
echo "===================="
echo ""

# Check Python version
echo "📌 Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "   Python version: $python_version"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python -m venv venv
    echo "   ✅ Virtual environment created"
else
    echo "   ✅ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo ""
echo "📥 Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "   ✅ Python dependencies installed"

# Install Tailwind dependencies
echo ""
echo "🎨 Installing Tailwind CSS..."
python manage.py tailwind install
echo "   ✅ Tailwind CSS installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "   ✅ .env file created"
    echo "   ⚠️  Please edit .env and add your OAuth credentials"
else
    echo ""
    echo "   ✅ .env file already exists"
fi

# Create logs directory
echo ""
echo "📁 Creating logs directory..."
mkdir -p logs
echo "   ✅ Logs directory created"

# Run migrations
echo ""
echo "🗄️  Running database migrations..."
python manage.py migrate
echo "   ✅ Database migrations completed"

# Ask if user wants to create superuser
echo ""
read -p "❓ Do you want to create a superuser? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Summary
echo ""
echo "✨ Setup Complete!"
echo "=================="
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Configure OAuth (if you haven't):"
echo "   - Visit: https://meta.wikimedia.org/wiki/Special:OAuthConsumerRegistration"
echo "   - Edit .env with your credentials"
echo ""
echo "2. Start the development servers:"
echo ""
echo "   Terminal 1 (Tailwind):"
echo "   $ python manage.py tailwind start"
echo ""
echo "   Terminal 2 (Django):"
echo "   $ python manage.py runserver"
echo ""
echo "3. Open your browser:"
echo "   http://127.0.0.1:8000/"
echo ""
echo "📚 Documentation:"
echo "   - Quick Start: QUICKSTART.md"
echo "   - Authentication: AUTHENTICATION_SETUP.md"
echo "   - Full Guide: README.md"
echo ""
echo "🎉 Happy coding!"
