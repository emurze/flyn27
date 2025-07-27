from flask import Flask, jsonify, Response

import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
)

from config import Config
from models import migrate, db
from routes import bp


def create_app() -> Flask:
    """Create and configure the Flask application."""

    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)
    flask_app.register_blueprint(bp)

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)

    @flask_app.route("/")
    def check_health() -> tuple[Response, int]:
        """Respond to health check requests."""
        return jsonify({"status": "ok"}), 200

    return flask_app


if __name__ == "__main__":
    app = create_app()
