import io
import json
import os
import sys
from collections.abc import Iterator

import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from werkzeug.test import TestResponse

# Add the source directory to the Python path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from app import create_app
from models import db as _db


@pytest.fixture
def app() -> Iterator[Flask]:
    """Create and configure a Flask app for testing."""
    app = create_app()

    with app.app_context():
        _db.drop_all()
        _db.create_all()
        yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Provides a test client for simulating HTTP requests."""
    return app.test_client()


@pytest.fixture
def runner(app: Flask) -> FlaskCliRunner:
    """Provides a test CLI runner for invoking Flask CLI commands."""
    return app.test_cli_runner()


def upload_json(client: FlaskClient, data: list[dict]) -> TestResponse:
    """Upload a JSON file via POST"""
    json_data = json.dumps(data)
    return client.post(
        "/",
        data={
            "json_file": (io.BytesIO(json_data.encode("utf-8")), "test.json")
        },
        content_type="multipart/form-data",
        follow_redirects=True,
    )
