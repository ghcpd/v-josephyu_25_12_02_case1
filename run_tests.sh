#!/bin/bash

##############################################################################
# Test Runner Script for Linux/macOS
# Runs all pytest tests with coverage and detailed reporting
##############################################################################

set -e

echo "=========================================="
echo "Flask User Management - Test Runner"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "ERROR: Virtual environment not found (.venv)"
    echo "Please run setup.sh first"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "ERROR: pytest not installed"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

echo "Running tests..."
echo ""

# Run all tests with verbose output and coverage
pytest test_auth.py test_config.py -v --tb=short --color=yes

TEST_RESULT=$?

echo ""
echo "=========================================="
if [ $TEST_RESULT -eq 0 ]; then
    echo "✓ All tests passed!" -ForegroundColor Green
else
    echo "✗ Some tests failed" -ForegroundColor Red
fi
echo "=========================================="
echo ""

# Run coverage report if available
if command -v coverage &> /dev/null; then
    echo "Generating coverage report..."
    coverage run -m pytest test_auth.py test_config.py --quiet
    coverage report --include="app.py,auth.py,models.py" 2>/dev/null || true
    echo ""
fi

exit $TEST_RESULT
