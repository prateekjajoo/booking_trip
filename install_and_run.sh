#!/bin/bash

# Step 1: Update package list and install pip if it's not installed
echo "Checking for pip installation..."

# Install pip if not present (for systems that don't have it)
if ! command -v pip &> /dev/null
then
    echo "pip not found. Installing pip..."
    python3 -m ensurepip --upgrade
else
    echo "pip is already installed."
fi

if [ -d "menv" ]; then
    echo "Activating virtual environment..."
    source menv/Scripts/activate
else
    echo "Virtual environment not found. create new virtual environment"
    python -m venv menv
    echo ""
    source menv/Scripts/activate
    echo "Virtual environment created."
fi

# Step 2: Install Python dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
else
    echo "No requirements.txt found, skipping installation of dependencies."
fi

# Step 3: Run the Flask app
echo "Running Flask app..."
#export FLASK_APP=Booking_app.py  # Change `app.py` to your Flask app filename if it's different
#export FLASK_ENV=development  # Optional: Set Flask to development mode (debug mode)
#flask run --host=0.0.0.0 --port=5000
python Booking_app.py