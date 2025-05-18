import pytest
import os
from fastapi.testclient import TestClient
from sqlite3 import Connection
from app.main import app
from app.utils.buffering import buffer
from app.utils.database import get_connection

TEST_DB_PATH = "tests/test.db"


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def db_connection():
    conn = get_connection()
    yield conn
    conn.close()


@pytest.fixture(scope="session", autouse=True)
def test_db_config():
    os.environ["DB_PATH"] = TEST_DB_PATH
    yield
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


@pytest.fixture(autouse=True)
def clean_buffer():
    buffer.clear()


@pytest.fixture(autouse=True)
def clean_db(db_connection: Connection):
    # Clean up database before each test
    db_connection.cursor().execute("DELETE FROM people")
    db_connection.commit()
