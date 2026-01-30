Param(
  [string]$VenvPath = ".venv"
)
$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir
python -m venv $VenvPath
$venvPython = Join-Path $VenvPath "Scripts/python.exe"
& $venvPython -m pip install -r requirements.txt
