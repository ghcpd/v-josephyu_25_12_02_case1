"""
Integration tests for complete user workflows
"""
import pytest
import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import init_db, get_connection


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


class TestCompleteUserJourney:
    """Test complete user workflows"""
    
    def test_complete_registration_to_dashboard_workflow(self, client):
        """Test: User Registration -> Login -> Dashboard -> Logout"""
        
        # Step 1: Get registration form
        response = client.get('/register')
        assert response.status_code == 200
        csrf_token = self._extract_csrf_token(response) or 'test-csrf-token'
        
        # Step 2: Register new user
        response = client.post('/register', data={
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'SecurePassword123!',
            'csrf_token': csrf_token
        }, follow_redirects=True)
        assert response.status_code == 200
        
        # Step 3: User should be redirected to dashboard after registration
        assert b'john_doe' in response.data or b'logged in' in response.data.lower()
        
        # Step 4: Logout
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        
        # Step 5: Try to access dashboard without authentication
        response = client.get('/dashboard')
        assert response.status_code == 302  # Redirect to login
        
        # Step 6: Login with registered credentials
        response = client.get('/login')
        csrf_token = self._extract_csrf_token(response)
        
        response = client.post('/login', data={
            'username': 'john_doe',
            'password': 'SecurePassword123!',
            'csrf_token': csrf_token
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'john_doe' in response.data
        
        # Step 7: Access dashboard successfully
        response = client.get('/dashboard')
        assert response.status_code == 200
        assert b'john_doe' in response.data
    
    def test_multiple_user_registration(self, client):
        """Test: Multiple users can register independently"""
        
        users = [
            {'username': 'alice', 'email': 'alice@example.com', 'password': 'pass123456'},
            {'username': 'bob', 'email': 'bob@example.com', 'password': 'pass123456'},
            {'username': 'charlie', 'email': 'charlie@example.com', 'password': 'pass123456'},
        ]
        
        for user in users:
            response = client.get('/register')
            csrf_token = self._extract_csrf_token(response)
            
            response = client.post('/register', data={
                'username': user['username'],
                'email': user['email'],
                'password': user['password'],
                'csrf_token': csrf_token
            }, follow_redirects=True)
            
            assert response.status_code == 200
            assert user['username'].encode() in response.data or b'logged in' in response.data.lower()
            
            # Logout for next user
            client.get('/logout', follow_redirects=True)
    
    def test_session_persistence_across_requests(self, client):
        """Test: User session persists across multiple requests"""
        
        # Register and login
        response = client.get('/register')
        csrf_token = self._extract_csrf_token(response)
        
        client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123456',
            'csrf_token': csrf_token
        }, follow_redirects=True)
        
        # Make multiple requests - session should persist
        for i in range(3):
            response = client.get('/dashboard')
            assert response.status_code == 200
            assert b'testuser' in response.data
    
    def test_invalid_login_does_not_create_session(self, client):
        """Test: Invalid login attempt doesn't create authenticated session"""
        
        # Register a user
        response = client.get('/register')
        csrf_token = self._extract_csrf_token(response)
        client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'correctpass123',
            'csrf_token': csrf_token
        })
        
        # Logout
        client.get('/logout')
        
        # Try to login with wrong password
        response = client.get('/login')
        csrf_token = self._extract_csrf_token(response)
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword',
            'csrf_token': csrf_token
        })
        
        assert b'Invalid' in response.data or b'invalid' in response.data.lower()
        
        # Try to access dashboard - should be redirected
        response = client.get('/dashboard')
        assert response.status_code == 302
    
    def test_form_validation_errors_display_correctly(self, client):
        """Test: Form validation errors are displayed to user"""
        
        # Try to register with invalid email
        response = client.get('/register')
        csrf_token = self._extract_csrf_token(response)
        
        response = client.post('/register', data={
            'username': 'validuser',
            'email': 'not-an-email',
            'password': 'password123456',
            'csrf_token': csrf_token
        })
        
        assert response.status_code == 200
        assert b'text-danger' in response.data or b'error' in response.data.lower()
    
    def test_password_too_short_validation(self, client):
        """Test: Password minimum length validation"""
        
        response = client.get('/register')
        csrf_token = self._extract_csrf_token(response)
        
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'short',  # Less than 6 characters
            'csrf_token': csrf_token
        })
        
        assert response.status_code == 200
        # Should show validation error
        assert b'text-danger' in response.data or b'error' in response.data.lower()
    
    def test_duplicate_username_prevention(self, client):
        """Test: Cannot register with duplicate username"""
        
        # First registration
        response = client.get('/register')
        csrf_token = self._extract_csrf_token(response)
        client.post('/register', data={
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'password123456',
            'csrf_token': csrf_token
        })
        
        # Logout
        client.get('/logout')
        
        # Try to register with same username
        response = client.get('/register')
        csrf_token = self._extract_csrf_token(response)
        response = client.post('/register', data={
            'username': 'john_doe',
            'email': 'different@example.com',
            'password': 'password123456',
            'csrf_token': csrf_token
        })
        
        assert response.status_code == 200
        assert b'already taken' in response.data or b'taken' in response.data.lower()
    
    def test_duplicate_email_prevention(self, client):
        """Test: Cannot register with duplicate email"""
        
        # First registration
        response = client.get('/register')
        csrf_token = self._extract_csrf_token(response)
        client.post('/register', data={
            'username': 'user1',
            'email': 'shared@example.com',
            'password': 'password123456',
            'csrf_token': csrf_token
        })
        
        # Logout
        client.get('/logout')
        
        # Try to register with same email
        response = client.get('/register')
        csrf_token = self._extract_csrf_token(response)
        response = client.post('/register', data={
            'username': 'user2',
            'email': 'shared@example.com',
            'password': 'password123456',
            'csrf_token': csrf_token
        })
        
        assert response.status_code == 200
        assert b'already registered' in response.data or b'registered' in response.data.lower()
    
    def _extract_csrf_token(self, response):
        """Extract CSRF token from response"""
        data = response.data.decode('utf-8')
        import re
        match = re.search(r'name="csrf_token"\s+type="hidden"\s+value="([^"]+)"', data)
        if match:
            return match.group(1)
        return ''


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_username_with_special_characters(self, client):
        """Test: Username with special characters"""
        
        response = client.get('/register')
        csrf_token = self._extract_csrf_token(response)
        
        response = client.post('/register', data={
            'username': 'user_name-123',
            'email': 'test@example.com',
            'password': 'password123456',
            'csrf_token': csrf_token
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_very_long_username(self, client):
        """Test: Username at maximum length"""
        
        response = client.get('/register')
        csrf_token = self._extract_csrf_token(response)
        
        response = client.post('/register', data={
            'username': 'a' * 32,  # Max 32 characters
            'email': 'test@example.com',
            'password': 'password123456',
            'csrf_token': csrf_token
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_username_too_long_validation(self, client):
        """Test: Username exceeding maximum length"""
        
        response = client.get('/register')
        csrf_token = self._extract_csrf_token(response)
        
        response = client.post('/register', data={
            'username': 'a' * 33,  # Exceeds max 32 characters
            'email': 'test@example.com',
            'password': 'password123456',
            'csrf_token': csrf_token
        })
        
        assert response.status_code == 200
        # Should show validation error
        assert b'text-danger' in response.data or b'error' in response.data.lower()
    
    def test_empty_form_submission(self, client):
        """Test: Empty form submission"""
        
        response = client.get('/register')
        csrf_token = self._extract_csrf_token(response)
        
        response = client.post('/register', data={
            'username': '',
            'email': '',
            'password': '',
            'csrf_token': csrf_token
        })
        
        assert response.status_code == 200
        # Should show validation errors
        assert b'text-danger' in response.data or b'error' in response.data.lower()
    
    def _extract_csrf_token(self, response):
        """Extract CSRF token from response"""
        data = response.data.decode('utf-8')
        import re
        match = re.search(r'name="csrf_token"\s+type="hidden"\s+value="([^"]+)"', data)
        if match:
            return match.group(1)
        return ''


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
