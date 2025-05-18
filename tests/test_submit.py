import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).parent.parent)
)  # Add parent directory to sys.path to reuse modules/pkgs in app/

import requests
import os
import random
from concurrent.futures import ThreadPoolExecutor
from app.utils.config import BUFFER_SIZE

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
FIRST_NAMES = ["John", "Jane", "Michael", "Emily", "David"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones"]


def generate_person():
    return {
        "first_name": random.choice(FIRST_NAMES),
        "last_name": random.choice(LAST_NAMES),
    }


def test_submit():
    url = f"{BASE_URL}/submit/"
    data = [generate_person() for _ in range(5)]  # Submit 5 records per request

    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}, Response: {response.json()}")


def run_load_test(num_requests=20):

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(test_submit) for _ in range(num_requests)
        ]  # default to 20 requests x 5 records = 100 total
        for future in futures:
            future.result()  # Wait for all requests to complete


def verify_flush_occurred():
    url = f"{BASE_URL}/count/"
    count = requests.get(url).json()["count"]

    if count >= BUFFER_SIZE:
        print(f"\n✅ VERIFICATION: Found {count} records in database (flush worked)")
        return True
    else:
        print(f"\n❌ VERIFICATION: Only {count} records in database (flush failed)")
        return False


if __name__ == "__main__":
    print("Starting load test...")
    run_load_test(25)  # 25 requests x 5 records = 125 total records
    print("Test completed, should trigger at least one database flush")

    if verify_flush_occurred():
        print("✅ Test PASSED - Flush logic working correctly")
    else:
        print("❌ Test FAILED - Flush logic not working as expected")
