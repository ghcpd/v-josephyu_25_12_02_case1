##############################################################################
# Test Runner Script for Windows PowerShell
# Runs all pytest tests with coverage and detailed reporting
##############################################################################

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Flask User Management - Test Runner" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path ".venv")) {
    Write-Host "ERROR: Virtual environment not found (.venv)" -ForegroundColor Red
    Write-Host "Please run setup.ps1 first" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& ".venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Check if pytest is installed
$pytestExists = Get-Command pytest -ErrorAction SilentlyContinue
if (-not $pytestExists) {
    Write-Host "ERROR: pytest not installed" -ForegroundColor Red
    Write-Host "Please run: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

Write-Host "Running tests..." -ForegroundColor Cyan
Write-Host ""

# Run all tests with verbose output
pytest test_auth.py test_config.py -v --tb=short --color=yes
$testResult = $LASTEXITCODE

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
if ($testResult -eq 0) {
    Write-Host "✓ All tests passed!" -ForegroundColor Green
} else {
    Write-Host "✗ Some tests failed" -ForegroundColor Red
}
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Run coverage report if available
$coverageExists = Get-Command coverage -ErrorAction SilentlyContinue
if ($coverageExists) {
    Write-Host "Generating coverage report..." -ForegroundColor Cyan
    coverage run -m pytest test_auth.py test_config.py --quiet 2>&1 | Out-Null
    coverage report --include="app.py,auth.py,models.py" 2>&1 | Out-Null
    Write-Host ""
}

exit $testResult
