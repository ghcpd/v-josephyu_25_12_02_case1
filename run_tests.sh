#!/bin/bash
# run_tests.sh - Test runner script for Flask User Management application (Linux/Mac)

set -e  # Exit on error

echo "=========================================="
echo "Flask User Management - Running Tests"
echo "=========================================="
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Display Python and pytest versions
echo "Python version: $(python --version)"
echo "Pytest version: $(pytest --version)"
echo ""

# Clean up any existing test database files
echo "Cleaning up test artifacts..."
rm -f test_*.db
rm -f .pytest_cache -rf
echo ""

# Run tests with pytest
echo "Running pytest..."
echo "----------------------------------------"
pytest -v --tb=short --color=yes

# Capture exit code
EXIT_CODE=$?

echo ""
echo "----------------------------------------"

if [ $EXIT_CODE -eq 0 ]; then
    echo "✓ All tests passed!"
else
    echo "✗ Some tests failed. Exit code: $EXIT_CODE"
fi

echo ""
echo "To run tests with coverage:"
echo "  pytest --cov=. --cov-report=html"
echo ""
echo "To run specific test file:"
echo "  pytest tests/test_auth.py -v"
echo ""
echo "To run specific test:"
echo "  pytest tests/test_auth.py::TestLogin::test_login_success -v"
echo ""

exit $EXIT_CODE
