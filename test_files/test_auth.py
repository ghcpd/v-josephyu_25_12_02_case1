import os
from app import app as flask_app
from models import init_db, get_connection, User


def create_client(tmp_path):
    # configure testing DB and disable CSRF for functional tests
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    db_file = tmp_path / 'test.db'
    flask_app.config['DATABASE'] = str(db_file)
    # initialize DB for this test
    init_db(flask_app)
    return flask_app.test_client()


def test_model_user_creation_and_lookup(tmp_path):
    client = create_client(tmp_path)
    conn = get_connection(flask_app)
    u = User.create(conn, 'bob', 'passsecret', 'bob@example.com')
    assert u.username == 'bob'
    assert u.verify_password('passsecret') is True
    fetched = User.get_by_username(conn, 'bob')
    assert fetched is not None
    assert fetched.id == u.id
    conn.close()


def test_register_and_dashboard_access(tmp_path):
    client = create_client(tmp_path)

    # Register a new user via the Flask view
    resp = client.post('/register', data={
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'mypassword',
        'submit': 'Register'
    }, follow_redirects=True)

    # After successful registration the dashboard should render and include the username
    assert resp.status_code == 200
    assert b'Hello, <strong>alice</strong>!' in resp.data

    # Dashboard should be accessible while logged in
    resp2 = client.get('/dashboard')
    assert resp2.status_code == 200
    assert b'Hello, <strong>alice</strong>!' in resp2.data


def test_login_with_invalid_password(tmp_path):
    client = create_client(tmp_path)

    # Create a user directly in the DB
    conn = get_connection(flask_app)
    User.create(conn, 'chris', 'longenough', 'chris@example.com')
    conn.close()

    # Attempt login with wrong password
    # use a password that satisfies form length validators (>=6) but is incorrect
    resp = client.post('/login', data={'username': 'chris', 'password': 'badpass', 'submit': 'Login'}, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Invalid username or password' in resp.data
