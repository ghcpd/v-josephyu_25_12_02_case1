import re
import pytest
import tempfile
from pathlib import Path

from app import app as flask_app
from models import init_db

csrf_re = re.compile(r'name="csrf_token" type="hidden" value="([^"]+)"')


def get_csrf(client, path):
    rv = client.get(path)
    assert rv.status_code == 200
    m = csrf_re.search(rv.get_data(as_text=True))
    assert m, f"No csrf token found in {path}"
    return m.group(1)


@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test.db"
    flask_app.config['DATABASE'] = str(db_path)
    flask_app.config['WTF_CSRF_ENABLED'] = True
    init_db(flask_app)
    with flask_app.test_client() as client:
        yield client


def test_dashboard_requires_login(client):
    resp = client.get('/dashboard')
    assert resp.status_code == 302
    assert '/login' in resp.headers.get('Location', '')


def test_register_and_login_flow(client):
    csrf = get_csrf(client, '/register')
    resp = client.post('/register', data={
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'secret123',
        'csrf_token': csrf,
    }, follow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers['Location'] == '/dashboard'

    # after register, should be able to access dashboard
    resp2 = client.get('/dashboard')
    assert resp2.status_code == 200
    assert 'alice' in resp2.get_data(as_text=True)

    # logout
    client.get('/logout')

    # login
    csrf_login = get_csrf(client, '/login')
    resp_login = client.post('/login', data={
        'username': 'alice',
        'password': 'secret123',
        'csrf_token': csrf_login,
    }, follow_redirects=False)
    assert resp_login.status_code == 302
    assert resp_login.headers['Location'] == '/dashboard'


def test_readme_routes_missing(client):
    missing_paths = ['/signup', '/signin', '/profile', '/api/register', '/api/login']
    for p in missing_paths:
        resp = client.get(p)
        assert resp.status_code == 404


def test_password_min_length(client):
    csrf = get_csrf(client, '/register')
    resp = client.post('/register', data={
        'username': 'bob',
        'email': 'bob@example.com',
        'password': '12345',  # too short (<6)
        'csrf_token': csrf,
    }, follow_redirects=True)
    body = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert 'Field must be between 6 and 128 characters long' in body


def test_email_required(client):
    csrf = get_csrf(client, '/register')
    resp = client.post('/register', data={
        'username': 'charlie',
        'email': '',
        'password': 'validpass',
        'csrf_token': csrf,
    }, follow_redirects=True)
    body = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert 'This field is required' in body
