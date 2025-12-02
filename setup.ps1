Param(
  [string]$Python = "py -3",
  [string]$VenvDir = ".venv"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $VenvDir)) {
  Write-Host "[setup] Creating virtualenv at $VenvDir"
  & py -3 -m venv $VenvDir
} else {
  Write-Host "[setup] Reusing existing virtualenv at $VenvDir"
}

$venvPython = Join-Path $VenvDir "Scripts/python.exe"

& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r requirements.txt

Write-Host "✅ Environment ready. Activate with: `& $VenvDir\Scripts\Activate.ps1"
