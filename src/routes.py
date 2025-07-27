from flask import (
    request,
    render_template,
    redirect,
    url_for,
    flash,
    Blueprint,
    Response,
)
import json

from pydantic import ValidationError

import services
from schemas import EntryRead

bp = Blueprint("entries", __name__)


@bp.route("/", methods=["GET", "POST"])
def upload() -> str | Response:
    """
    Handle the upload of a JSON file containing entry data.

    - GET: Render the upload form.
    - POST: Process the uploaded JSON file.
        - Validates each item using EntryRead schema.
        - Collects validation errors and flashes them to the user.
        - On success, stores the validated entries via the services layer.

    Returns:
        - Rendered upload template (GET)
        - Redirect to upload or entries view (POST)
    """
    if request.method == "POST":
        file = request.files.get("json_file")
        if not file:
            flash("File not found.", "error")
            return redirect(url_for("entries.upload"))

        try:
            raw_data = json.load(file.stream)
        except json.JSONDecodeError:
            flash("Invalid JSON format.", "error")
            return redirect(url_for("entries.upload"))

        errors = []
        validated_entries = []

        for i, item in enumerate(raw_data):
            try:
                validated_entries.append(EntryRead(**item))
            except ValidationError as e:
                for err in e.errors():
                    loc = " -> ".join(str(x) for x in err["loc"])
                    msg = err["msg"]
                    errors.append(f"[#{i}] Field '{loc}': {msg}")
            except Exception as e:
                errors.append(f"[#{i}] {str(e)}")

        if errors:
            for err in errors:
                flash(err, "error")
            return redirect(url_for("entries.upload"))

        services.upload_entries(validated_entries)
        flash("Data uploaded successfully.", "success")
        return redirect(url_for("entries.get_entries"))

    return render_template("upload.html")


@bp.route("/entries")
def get_entries() -> str:
    """
    Display all uploaded entries in a table view.

    Fetches the data from the services layer and renders it
    using the 'entries.html' template.

    Returns:
        Rendered template with the list of entries.
    """
    entries = services.get_entries()
    return render_template("entries.html", entries=entries)
