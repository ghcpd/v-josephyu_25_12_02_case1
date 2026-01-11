"""
Pytest configuration and fixtures for Flask application testing.
"""
import os
import sys
import pytest
import tempfile

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app
from models import init_db, get_connection


@pytest.fixture
def app():
    """Create and configure a test Flask application instance."""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    flask_app.config['TESTING'] = True
    flask_app.config['DATABASE'] = db_path
    flask_app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    flask_app.config['SECRET_KEY'] = 'test-secret-key'
    
    # Initialize the database
    init_db(flask_app)
    
    yield flask_app
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner for the Flask application."""
    return app.test_cli_runner()


@pytest.fixture
def db_connection(app):
    """Provide a database connection for tests."""
    conn = get_connection(app)
    yield conn
    conn.close()


@pytest.fixture
def authenticated_client(client):
    """Create a test client with an authenticated user session."""
    # Register a test user
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    }, follow_redirects=True)
    
    # Login
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass123'
    }, follow_redirects=True)
    
    return client
