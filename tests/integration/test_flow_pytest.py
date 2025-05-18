import random
from concurrent.futures import ThreadPoolExecutor
from app.utils.buffering import buffer
from app.utils.config import BUFFER_SIZE

FIRST_NAMES = ["John", "Jane", "Michael", "Emily", "David"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones"]


def generate_person():
    return {
        "first_name": random.choice(FIRST_NAMES),
        "last_name": random.choice(LAST_NAMES),
    }


def test_load_testing(client, db_connection):
    test_data = [generate_person() for _ in range(5)]

    def submit_request():
        return client.post("/submit/", json=test_data)

    # Make 125 requests
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(submit_request) for _ in range(25)
        ]  # 25 requests x 5 records = 125 total
        results = [f.result() for f in futures]

    assert all(r.status_code == 202 for r in results)

    # Verify flush occurred by checking database
    records_count = (
        db_connection.cursor().execute("SELECT COUNT(*) FROM people").fetchone()[0]
    )
    assert records_count == BUFFER_SIZE
    assert len(buffer) == 25  # Buffer size should equal (125-100)=25 after flush
