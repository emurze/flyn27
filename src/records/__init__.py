from flask import Blueprint

records_bp = Blueprint(
    "records",
    __name__,
    template_folder="templates",
    url_prefix="",
)


from . import routes
