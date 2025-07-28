import io

from flask.testing import FlaskClient

from tests.conftest import upload_json


def test_can_upload_valid_json(client: FlaskClient) -> None:
    # act
    response = upload_json(
        client,
        [
            {"name": "Alice", "date": "2025-07-27_14:30"},
            {"name": "Bob", "date": "2025-07-27_15:00"},
        ],
    )
    data = str(response.data)

    # assert
    assert response.status_code == 200
    assert "Alice" in data
    assert "Bob" in data
    assert "2025-07-27_15:00" in data
    assert "2025-07-27_14:30" in data


def test_cannot_upload_when_date_is_malformed(client: FlaskClient) -> None:
    # act
    response = upload_json(
        client,
        [
            {"name": "Charlie", "date": "202507271530"},
        ],
    )
    data = str(response.data)

    # assert
    assert response.status_code == 200
    assert "Date must be in &#39;YYYY-MM-DD_HH:mm&#39; format." in data


def test_cannot_upload_when_name_is_empty(client: FlaskClient) -> None:
    # act
    response = upload_json(
        client,
        [
            {"name": "", "date": "2025-07-27T14:30"},
        ],
    )

    # assert
    assert response.status_code == 200
    assert "Name cannot be empty." in str(response.data)


def test_cannot_upload_when_name_is_too_long(client: FlaskClient) -> None:
    # act
    response = upload_json(
        client,
        [
            {"name": "A" * 50, "date": "2025-07-27_14:30"},
        ],
    )

    # assert
    assert response.status_code == 200
    assert "Name is too long" in str(response.data)


def test_cannot_upload_when_name_is_not_in_entry(client: FlaskClient) -> None:
    # act
    response = upload_json(
        client,
        [
            {"date": "2025-07-27_14:30"},
        ],
    )

    # assert
    assert response.status_code == 200
    assert "Field &#39;name&#39;: Field required" in str(response.data)


def test_cannot_upload_when_no_file_provided(client: FlaskClient) -> None:
    # act
    response = client.post("/", data={}, follow_redirects=True)

    # assert
    assert "File not found." in str(response.data)


def test_cannot_upload_when_json_is_malformed(client: FlaskClient) -> None:
    # act
    bad_json = b'[{"name": "Alice", "date": "2025-07-27_14:30"'
    response = client.post(
        "/",
        data={"json_file": (io.BytesIO(bad_json), "bad.json")},
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    # assert
    assert "Invalid JSON format." in str(response.data)
