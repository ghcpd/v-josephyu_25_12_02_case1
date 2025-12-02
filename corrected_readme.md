# Flask User Management — Corrected Quick Start

This project is a small Flask user management example with registration, login and a protected dashboard.

Recommended environment: create and use a virtual environment named `.venv`.

Windows (PowerShell) setup

```powershell
# create the venv
python -m venv .venv

# activate in PowerShell
.\.venv\Scripts\Activate.ps1

# install dependencies
pip install -r requirements.txt
```

Unix / WSL / macOS setup

```bash
# create the venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the app (development)

You can run the app directly with Python (default host 127.0.0.1:5000):

```bash
python app.py
```

Or use the Flask CLI and specify a host/port:

```bash
set FLASK_APP=app.py      # Windows (PowerShell: $env:FLASK_APP = 'app.py')
flask run --host=0.0.0.0 --port=8080
```

Routes and forms

- Registration page: `/register` (form fields: username, email, password). Email is required.
- Login page: `/login` (form fields: username, password).
- Dashboard (protected): `/dashboard` — available after login.
- Logout: `/logout`

Notes

- The application uses `app.config['SECRET_KEY']` (set in `app.py`) for session/CSRF protection. The README previously referenced `FLASK_SECRET` — this project uses `SECRET_KEY` directly.
- The database file is `app.db` by default (in workspace root). The README previously mentioned `data/database.sqlite3` — that path is not used.
- There are no Redis or server-side session stores configured — the session is signed by Flask's SECRET_KEY.
- Password validation requires at least 6 characters (forms are configured in `auth.py`).

Testing

Install dev/test dependencies in your venv and run tests with pytest or use the helper scripts included in the repo:

```bash
# run tests directly
pytest -q test_files

# or use the helper scripts
./run_tests.sh       # bash / Unix
./run_tests.ps1      # PowerShell
```
