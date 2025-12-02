Param(
  [string]$VenvPython = ".venv/Scripts/python.exe",
  [string[]]$PytestArgs = @()
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $VenvPython)) {
  Write-Error "Venv python not found at $VenvPython. Run setup.ps1 first."
}

& $VenvPython -m pytest test_files @PytestArgs
