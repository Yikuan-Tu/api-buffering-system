import pytest


def test_submit_endpoint(client):
    test_data = [{"first_name": "Test", "last_name": "User"}]

    response = client.post("/submit/", json=test_data)
    assert response.status_code == 202
    assert response.json() == {"message": "Data received and being processed"}


def test_submit_empty_data(client):
    response = client.post("/submit/", json=[])
    assert response.status_code == 202


def test_submit_invalid_data(client):
    response = client.post("/submit/", json=[{"invalid": "data"}])
    assert response.status_code == 422  # Validation error


@pytest.mark.parametrize("count", [1, 5, 10])
def test_submit_multiple_records(client, count):
    test_data = [{"first_name": f"User{i}", "last_name": "Test"} for i in range(count)]
    response = client.post("/submit/", json=test_data)
    assert response.status_code == 202
