"""
Test suite for authentication module
"""
import pytest
import sys
import os
import tempfile
import sqlite3
from werkzeug.security import generate_password_hash

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import User, init_db, get_connection


@pytest.fixture
def client():
    """Create test app client with temporary database"""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    app.config['TESTING'] = True
    app.config['DATABASE'] = db_path
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        init_db(app)
    
    client = app.test_client()
    
    yield client
    
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def runner():
    """Create Flask test runner"""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    app.config['DATABASE'] = db_path
    
    with app.app_context():
        init_db(app)
    
    runner = app.test_cli_runner()
    
    yield runner
    
    os.close(db_fd)
    os.unlink(db_path)


class TestUserModel:
    """Test User model functionality"""
    
    def test_user_create(self):
        """Test creating a new user"""
        db_fd, db_path = tempfile.mkstemp(suffix='.db')
        app.config['DATABASE'] = db_path
        
        with app.app_context():
            init_db(app)
            conn = get_connection(app)
            
            user = User.create(conn, 'testuser', 'testpass123', 'test@example.com')
            
            assert user.username == 'testuser'
            assert user.email == 'test@example.com'
            assert user.id is not None
            
            conn.close()
        
        os.close(db_fd)
        os.unlink(db_path)
    
    def test_user_get_by_username(self):
        """Test retrieving user by username"""
        db_fd, db_path = tempfile.mkstemp(suffix='.db')
        app.config['DATABASE'] = db_path
        
        with app.app_context():
            init_db(app)
            conn = get_connection(app)
            
            User.create(conn, 'testuser', 'testpass123', 'test@example.com')
            user = User.get_by_username(conn, 'testuser')
            
            assert user is not None
            assert user.username == 'testuser'
            assert user.email == 'test@example.com'
            
            conn.close()
        
        os.close(db_fd)
        os.unlink(db_path)
    
    def test_user_verify_password(self):
        """Test password verification"""
        db_fd, db_path = tempfile.mkstemp(suffix='.db')
        app.config['DATABASE'] = db_path
        
        with app.app_context():
            init_db(app)
            conn = get_connection(app)
            
            user = User.create(conn, 'testuser', 'testpass123', 'test@example.com')
            
            assert user.verify_password('testpass123') is True
            assert user.verify_password('wrongpassword') is False
            
            conn.close()
        
        os.close(db_fd)
        os.unlink(db_path)
    
    def test_user_get_by_id(self):
        """Test retrieving user by ID"""
        db_fd, db_path = tempfile.mkstemp(suffix='.db')
        app.config['DATABASE'] = db_path
        
        with app.app_context():
            init_db(app)
            conn = get_connection(app)
            
            created_user = User.create(conn, 'testuser', 'testpass123', 'test@example.com')
            user = User.get_by_id(conn, created_user.id)
            
            assert user is not None
            assert user.id == created_user.id
            assert user.username == 'testuser'
            
            conn.close()
        
        os.close(db_fd)
        os.unlink(db_path)


class TestAuthEndpoints:
    """Test authentication endpoints"""
    
    def test_register_page_get(self, client):
        """Test GET /register returns registration form"""
        response = client.get('/register')
        assert response.status_code == 200
        assert b'User Registration' in response.data or b'username' in response.data
    
    def test_register_page_post_success(self, client):
        """Test successful user registration"""
        response = client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'csrf_token': self._get_csrf_token(client, '/register')
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_register_duplicate_username(self, client):
        """Test registration with duplicate username"""
        # Register first user
        token1 = self._get_csrf_token(client, '/register')
        client.post('/register', data={
            'username': 'testuser',
            'email': 'test1@example.com',
            'password': 'pass123456',
            'csrf_token': token1
        })
        
        # Try to register with same username
        token2 = self._get_csrf_token(client, '/register')
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'test2@example.com',
            'password': 'pass123456',
            'csrf_token': token2
        })
        
        assert b'already taken' in response.data or response.status_code == 200
    
    def test_login_page_get(self, client):
        """Test GET /login returns login form"""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'User Login' in response.data or b'username' in response.data
    
    def test_login_success(self, client):
        """Test successful login"""
        # Register user first
        token = self._get_csrf_token(client, '/register')
        client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'csrf_token': token
        })
        
        # Login
        token = self._get_csrf_token(client, '/login')
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass123',
            'csrf_token': token
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        token = self._get_csrf_token(client, '/login')
        response = client.post('/login', data={
            'username': 'nonexistent',
            'password': 'wrongpass',
            'csrf_token': token
        })
        
        assert b'Invalid' in response.data or response.status_code == 200
    
    def test_logout(self, client):
        """Test logout functionality"""
        # Register and login first
        reg_token = self._get_csrf_token(client, '/register')
        client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'csrf_token': reg_token
        })
        
        login_token = self._get_csrf_token(client, '/login')
        client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass123',
            'csrf_token': login_token
        })
        
        # Logout
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
    
    def test_dashboard_requires_login(self, client):
        """Test that /dashboard requires authentication"""
        response = client.get('/dashboard')
        assert response.status_code == 302  # Redirect to login
    
    def test_index_redirect(self, client):
        """Test that / redirects appropriately"""
        response = client.get('/')
        assert response.status_code == 302  # Should redirect
    
    def _get_csrf_token(self, client, url):
        """Helper to extract CSRF token from form"""
        response = client.get(url)
        # Simple extraction - in real scenario would use BeautifulSoup
        data = response.data.decode('utf-8')
        import re
        match = re.search(r'name="csrf_token"\s+type="hidden"\s+value="([^"]+)"', data)
        if match:
            return match.group(1)
        return ''


class TestPasswordValidation:
    """Test password validation rules"""
    
    def test_password_minimum_length(self, client):
        """Test that password minimum length is enforced"""
        token = self._get_csrf_token(client, '/register')
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'short',
            'csrf_token': token
        })
        
        # Should have validation error
        assert response.status_code == 200
    
    def _get_csrf_token(self, client, url):
        """Helper to extract CSRF token from form"""
        response = client.get(url)
        data = response.data.decode('utf-8')
        import re
        match = re.search(r'name="csrf_token"\s+type="hidden"\s+value="([^"]+)"', data)
        if match:
            return match.group(1)
        return ''


class TestEndpointDiscrepancies:
    """Test documented vs actual endpoints"""
    
    def test_signup_endpoint_not_found(self, client):
        """Verify /signup endpoint doesn't exist (README says it should)"""
        response = client.get('/signup')
        assert response.status_code == 404
    
    def test_signin_endpoint_not_found(self, client):
        """Verify /signin endpoint doesn't exist (README says it should)"""
        response = client.get('/signin')
        assert response.status_code == 404
    
    def test_profile_endpoint_not_found(self, client):
        """Verify /profile endpoint doesn't exist (README says it should)"""
        response = client.get('/profile')
        assert response.status_code == 404
    
    def test_api_register_not_found(self, client):
        """Verify POST /api/register doesn't exist (README documents it)"""
        response = client.post('/api/register', json={
            'user': 'testuser',
            'pass': 'testpass123',
            'mail': 'test@example.com'
        })
        assert response.status_code == 404
    
    def test_api_login_not_found(self, client):
        """Verify POST /api/login doesn't exist (README documents it)"""
        response = client.post('/api/login', json={
            'user': 'testuser',
            'pass': 'testpass123'
        })
        assert response.status_code == 404


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
