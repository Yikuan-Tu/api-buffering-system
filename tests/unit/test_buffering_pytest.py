import pytest
from app.utils.buffering import buffer_data, buffer
from app.models import Person


@pytest.fixture
def sample_person():
    return Person(first_name="Test", last_name="User")


def test_buffer_data(sample_person):
    # Add a single record
    count = buffer_data([sample_person])
    assert count == 1
    assert len(buffer) == 1


def test_flush_to_db(sample_person, db_connection):
    # Add a mount of BUFFER_SIZE records to trigger flush
    buffer.clear()
    records = [sample_person] * 100  # Default BUFFER_SIZE=100
    buffer_data(records)

    # Verify flush occurred by checking database
    count = db_connection.cursor().execute("SELECT COUNT(*) FROM people").fetchone()[0]
    assert count == 100
    assert len(buffer) == 0  # Buffer should be cleared after flush
