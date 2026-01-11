"""
Tests for authentication routes (login, register, logout).
"""
import pytest
from flask import session


class TestRegistration:
    """Test cases for user registration."""
    
    def test_register_page_loads(self, client):
        """Test that registration page loads successfully."""
        response = client.get('/register')
        assert response.status_code == 200
        assert b'User Registration' in response.data
    
    def test_register_success(self, client):
        """Test successful user registration."""
        response = client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Should redirect to dashboard after successful registration
        assert b'Welcome' in response.data or b'Dashboard' in response.data
    
    def test_register_duplicate_username(self, client):
        """Test registration fails with duplicate username."""
        # Register first user
        client.post('/register', data={
            'username': 'duplicate',
            'email': 'user1@example.com',
            'password': 'password123'
        })
        
        # Try to register with same username
        response = client.post('/register', data={
            'username': 'duplicate',
            'email': 'user2@example.com',
            'password': 'password456'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'already taken' in response.data.lower()
    
    def test_register_duplicate_email(self, client):
        """Test registration fails with duplicate email."""
        # Register first user
        client.post('/register', data={
            'username': 'user1',
            'email': 'same@example.com',
            'password': 'password123'
        })
        
        # Try to register with same email
        response = client.post('/register', data={
            'username': 'user2',
            'email': 'same@example.com',
            'password': 'password456'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'already registered' in response.data.lower()
    
    def test_register_invalid_email(self, client):
        """Test registration fails with invalid email format."""
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'notanemail',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Invalid email address' in response.data or b'valid email' in response.data.lower()
    
    def test_register_short_username(self, client):
        """Test registration fails with username too short."""
        response = client.post('/register', data={
            'username': 'ab',  # Only 2 characters (min is 3)
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'at least 3 characters' in response.data.lower()
    
    def test_register_short_password(self, client):
        """Test registration fails with password too short."""
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': '12345'  # Only 5 characters (min is 6)
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'at least 6 characters' in response.data.lower()
    
    def test_register_missing_fields(self, client):
        """Test registration fails with missing required fields."""
        response = client.post('/register', data={
            'username': 'testuser'
            # Missing email and password
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'required' in response.data.lower() or b'field' in response.data.lower()


class TestLogin:
    """Test cases for user login."""
    
    def test_login_page_loads(self, client):
        """Test that login page loads successfully."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'User Login' in response.data or b'Login' in response.data
    
    def test_login_success(self, client):
        """Test successful login."""
        # First register a user
        client.post('/register', data={
            'username': 'logintest',
            'email': 'login@example.com',
            'password': 'password123'
        })
        
        # Logout
        client.get('/logout')
        
        # Now login
        response = client.post('/login', data={
            'username': 'logintest',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Welcome' in response.data or b'Dashboard' in response.data
    
    def test_login_invalid_username(self, client):
        """Test login fails with non-existent username."""
        response = client.post('/login', data={
            'username': 'nonexistent',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Invalid' in response.data or b'incorrect' in response.data.lower()
    
    def test_login_wrong_password(self, client):
        """Test login fails with incorrect password."""
        # Register a user
        client.post('/register', data={
            'username': 'passtest',
            'email': 'passtest@example.com',
            'password': 'correctpass'
        })
        
        # Logout
        client.get('/logout')
        
        # Try to login with wrong password
        response = client.post('/login', data={
            'username': 'passtest',
            'password': 'wrongpass'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Invalid' in response.data or b'incorrect' in response.data.lower()
    
    def test_login_short_password_validation(self, client):
        """Test login form validates password length."""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': '12345'  # Too short
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'at least 6 characters' in response.data.lower()
    
    def test_login_missing_fields(self, client):
        """Test login fails with missing fields."""
        response = client.post('/login', data={
            'username': 'testuser'
            # Missing password
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'required' in response.data.lower() or b'field' in response.data.lower()


class TestLogout:
    """Test cases for user logout."""
    
    def test_logout_success(self, authenticated_client):
        """Test successful logout."""
        response = authenticated_client.get('/logout', follow_redirects=True)
        
        assert response.status_code == 200
        # Should redirect to login page
        assert b'Login' in response.data
    
    def test_logout_requires_login(self, client):
        """Test logout redirects unauthenticated users."""
        response = client.get('/logout', follow_redirects=True)
        
        # Should redirect to login page
        assert response.status_code == 200
        assert b'Login' in response.data


class TestAuthenticationFlow:
    """Test complete authentication workflows."""
    
    def test_register_and_login_flow(self, client):
        """Test complete flow: register, logout, login."""
        # 1. Register
        response = client.post('/register', data={
            'username': 'flowtest',
            'email': 'flow@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        assert response.status_code == 200
        
        # 2. Logout
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'Login' in response.data
        
        # 3. Login
        response = client.post('/login', data={
            'username': 'flowtest',
            'password': 'password123'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Welcome' in response.data or b'Dashboard' in response.data
    
    def test_protected_route_redirect(self, client):
        """Test that protected routes redirect to login."""
        response = client.get('/dashboard', follow_redirects=True)
        
        # Should redirect to login
        assert response.status_code == 200
        assert b'Login' in response.data
    
    def test_authenticated_access_dashboard(self, authenticated_client):
        """Test authenticated user can access dashboard."""
        response = authenticated_client.get('/dashboard')
        
        assert response.status_code == 200
        assert b'Welcome' in response.data or b'testuser' in response.data
    
    def test_root_redirect_unauthenticated(self, client):
        """Test root URL redirects to login when not authenticated."""
        response = client.get('/', follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Login' in response.data
    
    def test_root_redirect_authenticated(self, authenticated_client):
        """Test root URL redirects to dashboard when authenticated."""
        response = authenticated_client.get('/', follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Welcome' in response.data or b'Dashboard' in response.data
