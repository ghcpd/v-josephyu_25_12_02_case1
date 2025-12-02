#!/bin/bash
# setup.sh - Setup script for Flask User Management application (Linux/Mac)

set -e  # Exit on error

echo "=========================================="
echo "Flask User Management - Environment Setup"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

# Display Python version
PYTHON_VERSION=$(python3 --version)
echo "Found: $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "Virtual environment already exists. Skipping creation."
else
    python3 -m venv .venv
    echo "Virtual environment created successfully."
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo "Virtual environment activated."
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "Pip upgraded successfully."
echo ""

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt --quiet
echo "Dependencies installed successfully."
echo ""

# Display installed packages
echo "Installed packages:"
pip list
echo ""

# Initialize database (will be created on first run)
echo "Database will be initialized automatically on first run."
echo ""

echo "=========================================="
echo "Setup completed successfully!"
echo "=========================================="
echo ""
echo "To start the application:"
echo "  1. Activate the virtual environment:"
echo "     source .venv/bin/activate"
echo "  2. Run the application:"
echo "     python app.py"
echo "  3. Open http://127.0.0.1:5000 in your browser"
echo ""
echo "To run tests:"
echo "  bash run_tests.sh"
echo ""
