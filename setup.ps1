##############################################################################
# Flask App Setup Script for Windows PowerShell
# This script sets up the Python virtual environment and installs dependencies
##############################################################################

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Flask User Management - Setup Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
$pythonExists = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonExists) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or later from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

$pythonVersion = python --version 2>&1
Write-Host "✓ Found Python: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Create virtual environment
Write-Host "Creating Python virtual environment (.venv)..." -ForegroundColor Cyan
if (Test-Path ".venv") {
    Write-Host "  Virtual environment already exists, skipping creation" -ForegroundColor Yellow
} else {
    python -m venv .venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& ".venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip --quiet
Write-Host "✓ pip upgraded" -ForegroundColor Green
Write-Host ""

# Install requirements
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Cyan
if (-not (Test-Path "requirements.txt")) {
    Write-Host "ERROR: requirements.txt not found" -ForegroundColor Red
    exit 1
}

pip install -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Create database directory (if using corrected path)
Write-Host "Setting up database..." -ForegroundColor Cyan
if (-not (Test-Path "app.db")) {
    Write-Host "  Database will be created on first run" -ForegroundColor Yellow
} else {
    Write-Host "✓ Database file already exists (app.db)" -ForegroundColor Green
}
Write-Host ""

# Test the installation
Write-Host "Testing installation..." -ForegroundColor Cyan
python -c "import flask; print('  Flask version:', flask.__version__)"
python -c "import flask_login; print('  Flask-Login version:', flask_login.__version__)"
python -c "import flask_wtf; print('  Flask-WTF version:', flask_wtf.__version__)"
Write-Host "✓ All dependencies verified" -ForegroundColor Green
Write-Host ""

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Virtual environment is already activated" -ForegroundColor White
Write-Host ""
Write-Host "  2. Run the application:" -ForegroundColor White
Write-Host "     python app.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "  3. Open your browser to:" -ForegroundColor White
Write-Host "     http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "  4. Run tests:" -ForegroundColor White
Write-Host "     .\run_tests.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
