"""
Tests for database models and User class functionality.
"""
import pytest
from models import User, get_connection


class TestUserModel:
    """Test cases for the User model."""
    
    def test_user_creation(self, app, db_connection):
        """Test creating a new user."""
        user = User.create(
            db_connection,
            username='newuser',
            password='password123',
            email='newuser@example.com'
        )
        
        assert user.id is not None
        assert user.username == 'newuser'
        assert user.email == 'newuser@example.com'
        assert user.password_hash is not None
        assert user.password_hash != 'password123'  # Should be hashed
    
    def test_user_password_hashing(self, app, db_connection):
        """Test that passwords are properly hashed."""
        user = User.create(
            db_connection,
            username='hashtest',
            password='mypassword',
            email='hash@example.com'
        )
        
        # Password should be hashed (bcrypt format starts with $2b$)
        assert user.password_hash.startswith('$2b$')
        assert len(user.password_hash) >= 60
    
    def test_user_password_verification(self, app, db_connection):
        """Test password verification."""
        user = User.create(
            db_connection,
            username='verifytest',
            password='correctpassword',
            email='verify@example.com'
        )
        
        # Correct password should verify
        assert user.verify_password('correctpassword') is True
        
        # Incorrect password should not verify
        assert user.verify_password('wrongpassword') is False
    
    def test_get_user_by_username(self, app, db_connection):
        """Test retrieving a user by username."""
        # Create a user
        created_user = User.create(
            db_connection,
            username='findme',
            password='pass123',
            email='findme@example.com'
        )
        
        # Retrieve the user
        found_user = User.get_by_username(db_connection, 'findme')
        
        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.username == 'findme'
        assert found_user.email == 'findme@example.com'
    
    def test_get_user_by_username_not_found(self, app, db_connection):
        """Test retrieving a non-existent user returns None."""
        user = User.get_by_username(db_connection, 'nonexistent')
        assert user is None
    
    def test_get_user_by_id(self, app, db_connection):
        """Test retrieving a user by ID."""
        # Create a user
        created_user = User.create(
            db_connection,
            username='idtest',
            password='pass123',
            email='idtest@example.com'
        )
        
        # Retrieve by ID
        found_user = User.get_by_id(db_connection, created_user.id)
        
        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.username == 'idtest'
    
    def test_get_user_by_id_not_found(self, app, db_connection):
        """Test retrieving a non-existent user by ID returns None."""
        user = User.get_by_id(db_connection, 99999)
        assert user is None
    
    def test_username_uniqueness(self, app, db_connection):
        """Test that duplicate usernames are prevented."""
        User.create(
            db_connection,
            username='unique',
            password='pass123',
            email='unique1@example.com'
        )
        
        # Attempting to create another user with same username should fail
        with pytest.raises(Exception):  # sqlite3.IntegrityError
            User.create(
                db_connection,
                username='unique',
                password='pass456',
                email='unique2@example.com'
            )
    
    def test_email_uniqueness(self, app, db_connection):
        """Test that duplicate emails are prevented."""
        User.create(
            db_connection,
            username='user1',
            password='pass123',
            email='same@example.com'
        )
        
        # Attempting to create another user with same email should fail
        with pytest.raises(Exception):  # sqlite3.IntegrityError
            User.create(
                db_connection,
                username='user2',
                password='pass456',
                email='same@example.com'
            )
    
    def test_user_is_authenticated(self, app, db_connection):
        """Test UserMixin is_authenticated property."""
        user = User.create(
            db_connection,
            username='authtest',
            password='pass123',
            email='auth@example.com'
        )
        
        # UserMixin provides is_authenticated property
        assert user.is_authenticated is True
    
    def test_user_is_active(self, app, db_connection):
        """Test UserMixin is_active property."""
        user = User.create(
            db_connection,
            username='activetest',
            password='pass123',
            email='active@example.com'
        )
        
        # UserMixin provides is_active property
        assert user.is_active is True
    
    def test_user_get_id(self, app, db_connection):
        """Test UserMixin get_id method."""
        user = User.create(
            db_connection,
            username='getidtest',
            password='pass123',
            email='getid@example.com'
        )
        
        # UserMixin provides get_id method that returns string
        assert user.get_id() == str(user.id)


class TestDatabase:
    """Test database initialization and connection."""
    
    def test_database_initialization(self, app):
        """Test that database tables are created."""
        conn = get_connection(app)
        cursor = conn.cursor()
        
        # Check users table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
        )
        result = cursor.fetchone()
        
        assert result is not None
        assert result[0] == 'users'
        
        conn.close()
    
    def test_users_table_schema(self, app, db_connection):
        """Test that users table has correct columns."""
        cursor = db_connection.cursor()
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        column_names = [col[1] for col in columns]
        
        assert 'id' in column_names
        assert 'username' in column_names
        assert 'password_hash' in column_names
        assert 'email' in column_names
