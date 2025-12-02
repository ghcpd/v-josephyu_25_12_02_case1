# Flask User Management — Corrected README

## Prerequisites
- Python 3.8+ (tested with 3.13)
- Virtual environment (.venv)

## Setup
### PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Bash
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Quick Start
```powershell
# PowerShell
.\.venv\Scripts\Activate.ps1
python app.py  # binds 127.0.0.1:5000
```
```bash
# Bash
source .venv/bin/activate
python app.py  # binds 127.0.0.1:5000
```

To bind a different host/port, use Flask CLI:
```powershell
$env:FLASK_APP = 'app.py'
.\.venv\Scripts\flask.exe run --host=0.0.0.0 --port=8080
```
```bash
FLASK_APP=app.py flask run --host=0.0.0.0 --port=8080
```

Open http://127.0.0.1:5000

## Routes & Forms
- GET/POST `/register` — fields: `username` (min 3, unique), `email` (required, unique), `password` (min 6)
- GET/POST `/login` — fields: `username`, `password`
- GET `/dashboard` — requires login; shows logged-in user
- GET `/logout`

> Not implemented: `/signup`, `/signin`, `/profile`, `/api/register`, `/api/login`

## CSRF & Secrets
- CSRF provided by Flask-WTF using `app.config['SECRET_KEY']`
- Update `app.py` to set a strong secret key (e.g., read from env)

## Database
- SQLite file: `app.db` in project root

## Sessions
- Flask signed cookies (no Redis)

## Testing
```powershell
# PowerShell
.\.venv\Scripts\Activate.ps1
./run_tests.ps1
```
```bash
# Bash
source .venv/bin/activate
./run_tests.sh
```

Pytest suite: `test_files/`
