# Flask User Management App

A minimal login/registration demo using Flask, Flask-Login, Flask-WTF, and SQLite (`app.db`).

## Prerequisites
- Python 3.9+ (tested on 3.13)
- Git (optional)

## Setup (.venv)

### Windows (PowerShell)
```powershell
py -3 -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -r requirements.txt
```

### macOS/Linux (bash/zsh)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

> The project pins dependencies in `requirements.txt` to match the reference `.venv`.

## Configuration
- `SECRET_KEY`: set via environment variable `FLASK_SECRET` (optional). Falls back to a hardcoded development key.
- `DATABASE`: SQLite file `app.db` at the project root.

## Run the app

### Option 1: Flask CLI (recommended)
```powershell
# Windows (PowerShell)
$env:FLASK_APP = "app"
flask run --host 0.0.0.0 --port 8080
```
```bash
# macOS/Linux
export FLASK_APP=app
flask run --host 0.0.0.0 --port 8080
```

### Option 2: Direct execution
```powershell
python app.py --host 0.0.0.0 --port 8080 --debug
```
```bash
python app.py --host 0.0.0.0 --port 8080 --debug
```

Open http://localhost:8080 (or the host/port you specified).

## Web Routes
- `GET /` → redirects to `/dashboard` when authenticated, otherwise `/login`
- `GET|POST /register` → create an account (fields: `username`, `email`, `password`)
- `GET|POST /login` → sign in (fields: `username`, `password`)
- `GET /dashboard` → protected page showing the logged-in username
- `GET /logout` → sign out

> Email is **required** and must be valid. Password minimum length is **6** characters.

## Example (happy path)
1. Visit `/register`
2. Submit a unique `username`, valid `email`, and password ≥ 6 chars
3. You’ll be redirected to `/dashboard`
4. Logout at `/logout`
5. Login again at `/login`

## Programmatic Usage (test client example)
```python
from app import app

client = app.test_client()
client.post('/register', data={
    'username': 'alice',
    'email': 'alice@example.com',
    'password': 'secret123'
}, follow_redirects=True)
resp = client.get('/dashboard')
print(resp.status_code)  # 200 when authenticated via test client session
```

## Database
- SQLite file `app.db`
- Table `users`: `id`, `username` (unique), `password_hash`, `email` (unique)

## Testing
- Pytest tests live in `test_files/`
- Run via `run_tests.sh` (bash) or `run_tests.ps1` (PowerShell)

```powershell
./run_tests.ps1
```
```bash
./run_tests.sh
```

## Known Differences vs Original README
- Routes `/signup`, `/signin`, `/profile` do **not** exist; use `/register`, `/login`, `/dashboard`.
- JSON APIs `/api/register` and `/api/login` are **not implemented**.
- Sessions use Flask’s signed cookies (no Redis).
- Database path is `app.db` (not `data/database.sqlite3`).