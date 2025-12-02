#!/bin/bash

##############################################################################
# Flask App Setup Script for Linux/macOS
# This script sets up the Python virtual environment and installs dependencies
##############################################################################

set -e  # Exit on any error

echo "=========================================="
echo "Flask User Management - Setup Script"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or later"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✓ Found Python: $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "Creating Python virtual environment (.venv)..."
if [ -d ".venv" ]; then
    echo "  Virtual environment already exists, skipping creation"
else
    python3 -m venv .venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ pip upgraded"
echo ""

# Install requirements
echo "Installing dependencies from requirements.txt..."
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt not found"
    exit 1
fi

pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create database directory (if using corrected path)
echo "Setting up database..."
if [ ! -f "app.db" ]; then
    echo "  Database will be created on first run"
else
    echo "✓ Database file already exists (app.db)"
fi
echo ""

# Test the installation
echo "Testing installation..."
python3 -c "import flask; print('  Flask version:', flask.__version__)"
python3 -c "import flask_login; print('  Flask-Login version:', flask_login.__version__)"
python3 -c "import flask_wtf; print('  Flask-WTF version:', flask_wtf.__version__)"
echo "✓ All dependencies verified"
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Activate virtual environment:"
echo "     source .venv/bin/activate"
echo ""
echo "  2. Run the application:"
echo "     python app.py"
echo ""
echo "  3. Open your browser to:"
echo "     http://127.0.0.1:5000"
echo ""
echo "  4. Run tests:"
echo "     ./run_tests.sh"
echo ""
echo "=========================================="
