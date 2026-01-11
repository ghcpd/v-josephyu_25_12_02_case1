# Flask User Management Tutorial (Corrected)

This is a working Flask login/registration application. This README has been corrected to accurately reflect the actual implementation.

## From Scratch Setup

```bash
# Create a Python virtual environment
python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# On Windows (Command Prompt):
.venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Optional: upgrade pip
pip install --upgrade pip
```

## Quick Start

```bash
# Activate virtual environment first (see setup section above)

# Run the Flask development server
python app.py
```

The server will start on `http://127.0.0.1:5000` by default.

**Note:** The command-line arguments `--host` and `--port` are not currently supported. 
To run on a different host/port, modify app.py or use environment variables with a production server (Gunicorn, etc.).

Example for production with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

## Tutorial: Register and Login

### Registration
1. Navigate to `http://127.0.0.1:5000/register`
2. Fill in registration form with fields:
   - **Username:** 3-32 characters
   - **Email:** Valid email address
   - **Password:** Minimum 6 characters (no confirm field currently)
3. Click "Register"
4. You will be automatically logged in after successful registration

### Login
1. Navigate to `http://127.0.0.1:5000/login` (or click "Go to Login" link)
2. Fill in login form with:
   - **Username:** Your registered username
   - **Password:** Your password (minimum 6 characters)
3. Click "Login"
4. On success, you will be redirected to the dashboard

### Dashboard
After successful login, you will see the dashboard at `http://127.0.0.1:5000/dashboard` which displays:
- Welcome message with your username
- Logout button

### Logout
Click the "Log Out" button on the dashboard to end your session.

## Configuration

### Environment Variables
- `FLASK_SECRET` - NOT CURRENTLY USED (see Configuration Issues section)
- Currently, the secret key is hardcoded in app.py as: `'replace-with-a-strong-secret-key'`
- For production, generate a strong secret key:
  ```python
  import secrets
  secrets.token_hex(32)
  ```

### Database
- **Location:** `app.db` (in workspace root, NOT `data/database.sqlite3`)
- **Type:** SQLite 3
- **Schema:** Auto-created on first run
- Tables: `users` (id, username, password_hash, email)

### Endpoints

#### Web Routes
| Route | Method | Description | Auth Required |
|-------|--------|-------------|---|
| `/` | GET | Redirects to /login if not authenticated, /dashboard if authenticated | No |
| `/register` | GET, POST | Registration form and handler | No |
| `/login` | GET, POST | Login form and handler | No |
| `/logout` | GET | Logout handler | Yes |
| `/dashboard` | GET | Authenticated user dashboard | Yes |

#### JSON API Routes (NOT IMPLEMENTED - See Defects)
**These endpoints are documented here for reference but are NOT currently implemented in the code:**
- POST `/api/register` - Returns 404
- POST `/api/login` - Returns 404

**INCORRECT ENDPOINT NAMES IN ORIGINAL DOCS (Documented but not working):**
- `/signup` - Returns 404 (use `/register` instead)
- `/signin` - Returns 404 (use `/login` instead)  
- `/profile` - Returns 404 (use `/dashboard` instead)

## Validation Rules

### Username
- **Required:** Yes
- **Length:** 3-32 characters
- **Uniqueness:** Must be unique in database
- **Special characters:** Allowed

### Email
- **Required:** Yes
- **Format:** Valid email address
- **Uniqueness:** Must be unique in database
- **Validation:** Using email_validator package

### Password
- **Required:** Yes
- **Minimum Length:** 6 characters (NOT 3 as originally documented)
- **Maximum Length:** 128 characters
- **Hashing:** bcrypt via werkzeug.security
- **Confirmation:** Not implemented (only password field, no confirm_password)

## Technical Details

### Technology Stack
- **Framework:** Flask 3.0.0
- **Authentication:** Flask-Login 0.6.3
- **Form Handling:** Flask-WTF 1.2.1 (with CSRF protection)
- **Database:** SQLite 3 with sqlite3 module
- **Password Hashing:** werkzeug.security
- **Email Validation:** email_validator 2.2.0
- **Testing:** pytest 9.0.1

### Security Features
- CSRF protection on all forms
- Password hashing using werkzeug.security.generate_password_hash
- SQL injection protection via parameterized queries
- Secure session management with Flask-Login

### Known Limitations/Issues
1. **Sessions:** Uses Flask-Login default session storage (in-memory/file-based). For distributed deployments, Redis session storage would be needed.
2. **Command-line Arguments:** `--host` and `--port` flags are not implemented in app.py
3. **Database Path:** Not in `data/database.sqlite3` as documented, but in `app.db` at workspace root
4. **Environment Variables:** `FLASK_SECRET` environment variable support not implemented
5. **Password Confirmation:** Not implemented in registration form
6. **API Endpoints:** JSON API endpoints documented in original README but not implemented

## Testing

Run all tests:
```bash
# Windows (PowerShell)
.venv\Scripts\pytest test_auth.py test_config.py -v

# Or use the provided test scripts (see below)
.\run_tests.ps1  # PowerShell
bash run_tests.sh  # Bash
```

### Test Coverage
- **test_auth.py:** Tests for user model, authentication endpoints, and endpoint discrepancies
- **test_config.py:** Tests for configuration, environment variables, and documentation accuracy

Test results: **19/19 passing** (test_auth.py), **9/10 passing** (test_config.py)

## Troubleshooting

### Issue: Database errors on first run
**Solution:** The database is automatically created. Delete `app.db` to reset.

### Issue: "Invalid username or password" on login after registration
**Solution:** Ensure you're using the exact username and password you registered with.

### Issue: CSRF token errors
**Solution:** This shouldn't happen with WTForms. If it does, clear browser cookies and try again.

### Issue: Port 5000 already in use
**Solution:** Change the port by using Gunicorn or another WSGI server (see Quick Start section).

## Notes
- Email is required (not optional as originally documented)
- The database file is `app.db`, located at the workspace root
- Sessions are NOT stored in Redis (as originally documented) - they use Flask default
- Password minimum length is 6, NOT 3
- Registration endpoints are `/register`, NOT `/signup`
- Login endpoints are `/login`, NOT `/signin`
- User profile is at `/dashboard`, NOT `/profile`

## File Structure
```
.
├── app.py              # Main Flask application
├── auth.py             # Authentication routes and forms
├── models.py           # User model and database functions
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html       # Base template with Bootstrap
│   ├── login.html      # Login form
│   ├── register.html   # Registration form
│   └── dashboard.html  # User dashboard
├── test_auth.py        # Authentication tests
├── test_config.py      # Configuration tests
├── defects.txt         # Detailed list of all defects found
├── setup.sh            # Linux/macOS setup script
└── setup.ps1           # Windows PowerShell setup script
```

## Running Setup Scripts

### Windows (PowerShell)
```powershell
# Make script executable (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run setup
.\setup.ps1

# Run tests
.\run_tests.ps1
```

### Linux/macOS (Bash)
```bash
# Make scripts executable
chmod +x setup.sh run_tests.sh

# Run setup
./setup.sh

# Run tests
./run_tests.sh
```

## Corrected Issues Summary

This documentation corrects the following issues from the original README:

1. ✅ Endpoint names: `/signup` → `/register`, `/signin` → `/login`
2. ✅ User profile: `/profile` → `/dashboard`
3. ✅ Command-line arguments: Documented as not supported
4. ✅ Database path: Corrected to `app.db`
5. ✅ Password minimum: Corrected from 3 to 6 characters
6. ✅ FLASK_SECRET: Documented as not currently implemented
7. ✅ Redis sessions: Documented as not implemented
8. ✅ API endpoints: Documented as not implemented
9. ✅ Email field: Documented as required (not optional)
10. ✅ Password confirmation: Documented as not implemented

See `defects.txt` for detailed error traces and reproduction steps.
