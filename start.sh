#!/bin/bash

# ComparAid Startup Script

echo "🛒 Starting ComparAid - Irish Grocery Price Comparison"
echo "===================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
python3 -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"

echo ""
echo "Starting ComparAid server..."
echo "Visit http://localhost:5000 to use the application"
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask application
python3 app.py