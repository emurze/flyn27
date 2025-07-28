from flask import Flask

import os
import sys

from werkzeug.middleware.proxy_fix import ProxyFix

# Add the source directory to the Python path
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

    flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app, x_for=1, x_proto=1)
    return flask_app


if __name__ == "__main__":
    app = create_app()
