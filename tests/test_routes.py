"""
Tests for application routes and integration testing.
"""
import pytest


class TestRoutes:
    """Test cases for application routes."""
    
    def test_index_route(self, client):
        """Test that index route exists and redirects."""
        response = client.get('/')
        # Should redirect (302) or show a page (200)
        assert response.status_code in [200, 302]
    
    def test_login_route_exists(self, client):
        """Test /login route exists."""
        response = client.get('/login')
        assert response.status_code == 200
    
    def test_register_route_exists(self, client):
        """Test /register route exists."""
        response = client.get('/register')
        assert response.status_code == 200
    
    def test_dashboard_route_exists(self, authenticated_client):
        """Test /dashboard route exists for authenticated users."""
        response = authenticated_client.get('/dashboard')
        assert response.status_code == 200
    
    def test_logout_route_exists(self, authenticated_client):
        """Test /logout route exists."""
        response = authenticated_client.get('/logout')
        # Should redirect after logout
        assert response.status_code in [200, 302]
    
    def test_nonexistent_route_404(self, client):
        """Test that non-existent routes return 404."""
        response = client.get('/nonexistent')
        assert response.status_code == 404
    
    def test_signup_route_not_found(self, client):
        """Test /signup route doesn't exist (should be /register)."""
        response = client.get('/signup')
        assert response.status_code == 404
    
    def test_signin_route_not_found(self, client):
        """Test /signin route doesn't exist (should be /login)."""
        response = client.get('/signin')
        assert response.status_code == 404
    
    def test_profile_route_not_found(self, client):
        """Test /profile route doesn't exist (should be /dashboard)."""
        response = client.get('/profile')
        assert response.status_code == 404
    
    def test_api_register_not_found(self, client):
        """Test /api/register endpoint doesn't exist."""
        response = client.post('/api/register', json={
            'user': 'test',
            'pass': '123',
            'mail': 'test@example.com'
        })
        assert response.status_code == 404
    
    def test_api_login_not_found(self, client):
        """Test /api/login endpoint doesn't exist."""
        response = client.post('/api/login', json={
            'user': 'test',
            'pass': '123'
        })
        assert response.status_code == 404


class TestTemplates:
    """Test template rendering and content."""
    
    def test_login_template_renders(self, client):
        """Test login template renders correctly."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'username' in response.data.lower()
        assert b'password' in response.data.lower()
    
    def test_register_template_renders(self, client):
        """Test register template renders correctly."""
        response = client.get('/register')
        assert response.status_code == 200
        assert b'username' in response.data.lower()
        assert b'email' in response.data.lower()
        assert b'password' in response.data.lower()
    
    def test_dashboard_template_renders(self, authenticated_client):
        """Test dashboard template renders correctly."""
        response = authenticated_client.get('/dashboard')
        assert response.status_code == 200
        assert b'testuser' in response.data
        assert b'Welcome' in response.data or b'Hello' in response.data
    
    def test_base_template_includes_bootstrap(self, client):
        """Test that base template includes Bootstrap CSS."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'bootstrap' in response.data.lower()
    
    def test_csrf_token_in_forms(self, client):
        """Test that CSRF token is included in forms."""
        response = client.get('/login')
        assert response.status_code == 200
        # Should have hidden CSRF token field
        assert b'csrf_token' in response.data or b'hidden' in response.data


class TestSessionManagement:
    """Test session handling."""
    
    def test_session_created_on_login(self, client):
        """Test that session is created when user logs in."""
        # Register and login
        client.post('/register', data={
            'username': 'sessiontest',
            'email': 'session@example.com',
            'password': 'password123'
        })
        
        with client.session_transaction() as sess:
            # Session should contain user_id after login
            assert '_user_id' in sess or 'user_id' in sess
    
    def test_session_cleared_on_logout(self, authenticated_client):
        """Test that session is cleared when user logs out."""
        # Logout
        authenticated_client.get('/logout')
        
        # Check session is cleared
        with authenticated_client.session_transaction() as sess:
            assert '_user_id' not in sess


class TestFlashMessages:
    """Test flash message functionality."""
    
    def test_flash_on_invalid_login(self, client):
        """Test flash message appears on invalid login."""
        response = client.post('/login', data={
            'username': 'nonexistent',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Invalid' in response.data
    
    def test_flash_on_duplicate_username(self, client):
        """Test flash message appears on duplicate username."""
        # Register first user
        client.post('/register', data={
            'username': 'duplicate',
            'email': 'user1@example.com',
            'password': 'password123'
        })
        
        # Try duplicate
        response = client.post('/register', data={
            'username': 'duplicate',
            'email': 'user2@example.com',
            'password': 'password456'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'taken' in response.data.lower()


class TestSecurityFeatures:
    """Test security features of the application."""
    
    def test_password_is_hashed(self, client, db_connection):
        """Test that passwords are stored as hashes, not plaintext."""
        # Register a user
        client.post('/register', data={
            'username': 'secureuser',
            'email': 'secure@example.com',
            'password': 'mypassword'
        })
        
        # Check database
        cursor = db_connection.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = ?", ('secureuser',))
        result = cursor.fetchone()
        
        assert result is not None
        password_hash = result[0]
        
        # Password should be hashed (not equal to plaintext)
        assert password_hash != 'mypassword'
        # Bcrypt hashes start with $2b$
        assert password_hash.startswith('$2b$')
    
    def test_email_is_stored(self, client, db_connection):
        """Test that email is properly stored in database."""
        # Register a user
        client.post('/register', data={
            'username': 'emailtest',
            'email': 'email@example.com',
            'password': 'password123'
        })
        
        # Check database
        cursor = db_connection.cursor()
        cursor.execute("SELECT email FROM users WHERE username = ?", ('emailtest',))
        result = cursor.fetchone()
        
        assert result is not None
        assert result[0] == 'email@example.com'


class TestDatabaseIntegration:
    """Test database integration with application."""
    
    def test_user_persists_after_registration(self, client, db_connection):
        """Test that user data persists in database."""
        # Register
        client.post('/register', data={
            'username': 'persisttest',
            'email': 'persist@example.com',
            'password': 'password123'
        })
        
        # Query database
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", ('persisttest',))
        result = cursor.fetchone()
        
        assert result is not None
    
    def test_multiple_users_can_register(self, client, db_connection):
        """Test that multiple users can be registered."""
        # Register multiple users
        users = [
            ('user1', 'user1@example.com', 'pass123'),
            ('user2', 'user2@example.com', 'pass456'),
            ('user3', 'user3@example.com', 'pass789'),
        ]
        
        for username, email, password in users:
            client.post('/register', data={
                'username': username,
                'email': email,
                'password': password
            })
        
        # Check all users exist
        cursor = db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        
        assert count >= 3


class TestFormValidation:
    """Test form validation across the application."""
    
    def test_email_validation_format(self, client):
        """Test email validation accepts valid formats."""
        valid_emails = [
            'test@example.com',
            'user.name@example.com',
            'user+tag@example.co.uk',
            'test_user@subdomain.example.com'
        ]
        
        for i, email in enumerate(valid_emails):
            response = client.post('/register', data={
                'username': f'emailvalid{i}',
                'email': email,
                'password': 'password123'
            }, follow_redirects=True)
            
            # Should not show email validation error
            assert b'Invalid email' not in response.data
    
    def test_username_length_validation(self, client):
        """Test username length is validated."""
        # Too short (< 3 characters)
        response = client.post('/register', data={
            'username': 'ab',
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert b'at least 3 characters' in response.data.lower()
    
    def test_password_length_validation(self, client):
        """Test password length is validated."""
        # Too short (< 6 characters)
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': '12345'
        }, follow_redirects=True)
        
        assert b'at least 6 characters' in response.data.lower()
