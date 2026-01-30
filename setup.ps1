<# PowerShell setup helper for the project #>
Write-Host "Creating virtual env .venv (if not exists)"
python -m venv .venv

Write-Host "Activating venv and installing dependencies"
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Initialized. Run: python app.py or flask run"
