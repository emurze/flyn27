from flask import Flask, jsonify, Response

from config import Config
from records import records_bp
from records.models import db, migrate


def create_app() -> Flask:
    """Create and configure the Flask application."""

    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(records_bp)
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/")
    def check_health() -> tuple[Response, int]:
        """Respond to health check requests."""
        return jsonify({"status": "ok"}), 200

    return app
