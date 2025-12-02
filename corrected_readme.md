# Flask User Management Tutorial (Corrected)

This is a corrected version of the README with accurate documentation that matches the actual implementation.

## From Scratch Setup

```bash
# Create a Python virtual environment
python -m venv .venv

# Activate on Linux/Mac:
source .venv/bin/activate

# Activate on Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Activate on Windows CMD:
.\.venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Optional: upgrade pip
pip install --upgrade pip
```

## Quick Start

```bash
# Basic usage (runs on http://127.0.0.1:5000 by default)
python app.py
```

The application runs on `http://127.0.0.1:5000` by default.

**Note:** Command-line arguments like `--host` and `--port` are not supported. To change host/port, modify `app.py` line 37:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

## Tutorial: Register and Login

### Web Interface

1. **Register a new user** at `/register` with the following fields:
   - `username` (required, 3-32 characters)
   - `email` (required, must be valid email format)
   - `password` (required, 6-128 characters)

2. **Login** at `/login` with:
   - `username` (required)
   - `password` (required)

3. **Access the dashboard** at `/dashboard` after logging in

4. **Logout** at `/logout`

### Route Summary

| Purpose | Route | Methods | Login Required |
|---------|-------|---------|----------------|
| Home | `/` | GET | No |
| Login | `/login` | GET, POST | No |
| Register | `/register` | GET, POST | No |
| Dashboard | `/dashboard` | GET | Yes |
| Logout | `/logout` | GET | Yes |

## Configuration

### Secret Key

The application uses a hardcoded secret key by default. For production:

```python
# In app.py, line 8
app.config['SECRET_KEY'] = 'replace-with-a-strong-secret-key'
```

To use an environment variable:

```python
import os
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'fallback-secret-key')
```

Then set the environment variable:
```bash
# Linux/Mac
export FLASK_SECRET='your-secret-key-here'

# Windows PowerShell
$env:FLASK_SECRET = 'your-secret-key-here'

# Windows CMD
set FLASK_SECRET=your-secret-key-here
```

### Database

- Database file: `app.db` (SQLite, created at workspace root)
- Location: Same directory as `app.py`
- The database is automatically created on first run

To use a different database location:
```python
# In app.py, line 9
app.config['DATABASE'] = 'path/to/your/database.db'
```

## Validation Rules

### Username
- Required field
- Minimum length: 3 characters
- Maximum length: 32 characters
- Must be unique

### Email
- Required field (NOT optional)
- Must be valid email format
- Maximum length: 255 characters
- Must be unique

### Password
- Required field
- Minimum length: 6 characters (NOT 3)
- Maximum length: 128 characters
- Stored as bcrypt hash

## Sessions

The application uses Flask's default session management (client-side encrypted cookies).
Sessions are NOT stored in Redis. The session cookie is signed with the SECRET_KEY.

## Testing

### Run All Tests

```bash
# Linux/Mac
bash run_tests.sh

# Windows PowerShell
.\run_tests.ps1
```

### Run Tests with pytest

```bash
pytest
pytest -v  # verbose output
pytest --cov  # with coverage report
```

## Project Structure

```
├── app.py                 # Main application file
├── auth.py                # Authentication blueprint (login, register, logout)
├── models.py              # Database models and User class
├── requirements.txt       # Python dependencies
├── app.db                 # SQLite database (created on first run)
├── templates/
│   ├── base.html         # Base template with Bootstrap
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   └── dashboard.html    # User dashboard
└── tests/
    ├── test_auth.py      # Authentication tests
    ├── test_models.py    # Database model tests
    └── test_routes.py    # Route and integration tests
```

## Dependencies

```
Flask==3.0.0              # Web framework
Flask-Login==0.6.3        # User session management
Flask-WTF==1.2.1          # Form handling and CSRF protection
WTForms==3.1.2            # Form validation
Werkzeug==3.0.1           # Password hashing
email_validator==2.2.0    # Email validation
pytest==9.0.1             # Testing framework
requests==2.32.3          # HTTP client for testing
```

## Common Issues

### 404 Not Found
- Make sure you use `/register` (not `/signup`)
- Make sure you use `/login` (not `/signin`)
- Make sure you use `/dashboard` (not `/profile`)

### Password Too Short
- Minimum password length is 6 characters, not 3

### Email Required
- Email field is mandatory for registration

### CSRF Token Missing
- The app uses Flask-WTF for CSRF protection
- Forms must include `{{ form.hidden_tag() }}` in templates
- Web browsers handle this automatically

## Development Notes

- Debug mode is enabled by default (`debug=True` in `app.py`)
- The database schema is automatically created on first run
- User passwords are hashed using Werkzeug's security functions (bcrypt)
- Flask-Login manages user sessions and provides `@login_required` decorator
- Bootstrap 5.3.2 is used for styling (loaded from CDN)

## Security Recommendations

For production deployment:

1. **Set a strong SECRET_KEY**: Use a random 32+ character string
2. **Disable debug mode**: Change `debug=False` in `app.run()`
3. **Use environment variables**: Don't hardcode secrets
4. **Use HTTPS**: Enable SSL/TLS
5. **Use a production WSGI server**: Such as Gunicorn or uWSGI
6. **Set secure cookie flags**: Configure `SESSION_COOKIE_SECURE = True`
7. **Use a production database**: Consider PostgreSQL instead of SQLite

## License

This is a tutorial/example project for educational purposes.
