from werkzeug.exceptions import HTTPException

from flask import Flask, jsonify, Response

from config import Config


def create_app() -> Flask:
    """Create and configure the Flask application."""

    app = Flask(__name__)
    app.config.from_object(Config)

    @app.errorhandler(Exception)
    def handle_exception(e: Exception) -> tuple[Response, int]:
        """Handle exceptions raised during request processing."""
        if isinstance(e, HTTPException):
            return jsonify({"error": e.description}), e.code
        return jsonify({"error": "Внутренняя ошибка сервера"}), 500

    @app.route("/")
    def check_health() -> tuple[Response, int]:
        """Respond to health check requests."""
        return jsonify({"status": "ok"}), 200

    return app
