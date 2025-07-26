import json
from datetime import datetime
from flask import render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename

from . import records_bp
from records.models import db, Record


def validate_json(data):
    if not isinstance(data, list):
        return False, "JSON should be a list"
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            return False, f"Item {idx} is not an object"
        if "name" not in item or "date" not in item:
            return False, f"Item {idx} missing 'name' or 'date'"
        name = item["name"]
        date_str = item["date"]
        if not isinstance(name, str):
            return False, f"Item {idx} 'name' is not a string"
        if len(name) >= 50:
            return False, f"Item {idx} 'name' length must be less than 50"
        if not isinstance(date_str, str):
            return False, f"Item {idx} 'date' is not a string"
        try:
            datetime.strptime(date_str, "%Y-%m-%d_%H:%M")
        except ValueError:
            return False, f"Item {idx} 'date' format invalid, expected YYYY-MM-DD_HH:mm"
    return True, None


@records_bp.route("/", methods=["GET", "POST"])
def upload_json():
    if request.method == "POST":
        if "json_file" not in request.files:
            flash(("Error", "No file part"))
            return redirect(request.url)
        file = request.files["json_file"]
        if file.filename == "":
            flash(("Error", "No selected file"))
            return redirect(request.url)
        filename = secure_filename(file.filename)
        try:
            data = json.load(file)
        except Exception as e:
            flash(("Error", f"Invalid JSON: {e}"))
            return redirect(request.url)
        valid, error = validate_json(data)
        if not valid:
            flash(("Error", error))
            return redirect(request.url)

        for item in data:
            rec = Record(
                name=item["name"],
                date=datetime.strptime(item["date"], "%Y-%m-%d_%H:%M"),
            )
            db.session.add(rec)
        db.session.commit()
        flash(("Success", f"Uploaded {len(data)} records successfully!"))
        return redirect(url_for("records.upload_json"))

    return render_template("upload.html")


@records_bp.route("/records")
def list_records():
    records = Record.query.order_by(Record.id.desc()).all()
    return render_template("list.html", records=records)
