from flask.testing import FlaskClient

from tests.conftest import upload_json


def test_can_get_entries(client: FlaskClient) -> None:
    # arrange
    upload_json(
        client,
        [
            {"name": "Alice", "date": "2025-07-27_14:30"},
            {"name": "Bob", "date": "2025-07-27_15:00"},
        ],
    )

    # act
    response = client.get("/entries")
    data = str(response.data)

    # assert
    assert response.status_code == 200
    assert "Alice" in data
    assert "Bob" in data
    assert "2025-07-27_15:00" in data
    assert "2025-07-27_14:30" in data
