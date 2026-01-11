# run_tests.ps1 - Test runner script for Flask User Management application (Windows PowerShell)

$ErrorActionPreference = "Continue"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Flask User Management - Running Tests" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".\.venv\Scripts\Activate.ps1"
}

# Display Python and pytest versions
try {
    $pythonVersion = python --version 2>&1
    $pytestVersion = pytest --version 2>&1
    Write-Host "Python version: $pythonVersion" -ForegroundColor Green
    Write-Host "Pytest version: $pytestVersion" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "Error: Could not determine Python or pytest version." -ForegroundColor Red
    exit 1
}

# Clean up any existing test database files
Write-Host "Cleaning up test artifacts..." -ForegroundColor Yellow
Remove-Item -Path "test_*.db" -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".pytest_cache" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host ""

# Run tests with pytest
Write-Host "Running pytest..." -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Gray

pytest -v --tb=short --color=yes
$EXIT_CODE = $LASTEXITCODE

# Display results
Write-Host ""
Write-Host "----------------------------------------" -ForegroundColor Gray

if ($EXIT_CODE -eq 0) {
    Write-Host "✓ All tests passed!" -ForegroundColor Green
} else {
    Write-Host "✗ Some tests failed. Exit code: $EXIT_CODE" -ForegroundColor Red
}

Write-Host ""
Write-Host "To run tests with coverage:" -ForegroundColor Cyan
Write-Host "  pytest --cov=. --cov-report=html" -ForegroundColor Gray
Write-Host ""
Write-Host "To run specific test file:" -ForegroundColor Cyan
Write-Host "  pytest tests/test_auth.py -v" -ForegroundColor Gray
Write-Host ""
Write-Host "To run specific test:" -ForegroundColor Cyan
Write-Host "  pytest tests/test_auth.py::TestLogin::test_login_success -v" -ForegroundColor Gray
Write-Host ""

exit $EXIT_CODE
