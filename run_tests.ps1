Param(
  [string]$VenvPath = ".venv",
  [string[]]$PytestArgs = @("test_files")
)
$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

if (-not (Test-Path $VenvPath)) {
  python -m venv $VenvPath
}
$venvPython = Join-Path $VenvPath "Scripts/python.exe"
& $venvPython -m pip install -r requirements.txt
& $venvPython -m pytest @PytestArgs
