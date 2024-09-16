import pytest
import sys
import os
import redis

# system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

# Setting up fixtures
@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# test redis instance
@pytest.fixture
def redis_client():
    client = redis.Redis(host='localhost', port=6379, db=1)
    
    yield client
    client.flushdb()
