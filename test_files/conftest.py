import os
import tempfile
import pytest

from app import app as flask_app
from models import init_db


@pytest.fixture()
def app():
    # Configure a temporary database for each test session
    db_fd, db_path = tempfile.mkstemp(prefix='test_app_', suffix='.db')
    os.close(db_fd)  # close fd; sqlite will create the file as needed

    flask_app.config['DATABASE'] = db_path
    flask_app.config['WTF_CSRF_ENABLED'] = False
    init_db(flask_app)

    yield flask_app

    # teardown
    try:
        os.remove(db_path)
    except FileNotFoundError:
        pass


@pytest.fixture()
def client(app):
    return app.test_client()
