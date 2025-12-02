import re

from models import get_connection, User


def register(client, username, email, password, follow_redirects=True):
    return client.post('/register', data={
        'username': username,
        'email': email,
        'password': password,
    }, follow_redirects=follow_redirects)


def login(client, username, password, follow_redirects=True):
    return client.post('/login', data={
        'username': username,
        'password': password,
    }, follow_redirects=follow_redirects)


def test_register_and_login_happy_path(app, client):
    resp = register(client, 'alice', 'alice@example.com', 'secret123')
    assert resp.status_code == 200
    assert b'Hello, <strong>alice</strong>' in resp.data

    # Logout and login again
    client.get('/logout', follow_redirects=True)
    resp = login(client, 'alice', 'secret123')
    assert resp.status_code == 200
    assert b'Hello, <strong>alice</strong>' in resp.data


def test_unique_username_and_email(app, client):
    register(client, 'alice', 'alice@example.com', 'secret123')

    # duplicate username
    resp = register(client, 'alice', 'alice2@example.com', 'secret123')
    assert resp.status_code == 200
    assert b'Username is already taken' in resp.data

    # duplicate email
    resp = register(client, 'bob', 'alice@example.com', 'secret123')
    assert resp.status_code == 200
    assert b'Email is already registered' in resp.data


def test_login_invalid_credentials(app, client):
    register(client, 'alice', 'alice@example.com', 'secret123')

    resp = login(client, 'alice', 'wrongpass')
    assert resp.status_code == 200
    assert b'Invalid username or password' in resp.data


def test_dashboard_requires_login(app, client):
    resp = client.get('/dashboard')
    assert resp.status_code in (301, 302)
    # Follow redirect to login page
    resp = client.get('/dashboard', follow_redirects=True)
    assert resp.status_code == 200
    assert b'User Login' in resp.data
