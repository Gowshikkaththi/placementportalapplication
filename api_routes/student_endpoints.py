from flask import Blueprint, jsonify,request
from flasgger import swag_from
from controller_impl.student_impl import *
from config.swagger import *
from config.db_creation import db_session
from config.decorators import role_required


student_api = Blueprint("student_api", __name__)

@student_api.route("/dashboard")
def student_dashboard():
    from flask import session, render_template
    return render_template(
        "student_dashboard.html",
        student_id=session["table_id"]
    )

@student_api.route("/drives/<int:student_id>", methods=["GET"])
@swag_from(get_approved_drives_swagger)
@role_required("STUDENT")
def fetch_approved_drives(student_id):

    result = get_approved_drives(db_session,student_id)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 500

    return jsonify(result), 200



@student_api.route("/apply", methods=["POST"])
@swag_from(apply_for_drive_swagger)
@role_required("STUDENT")
def apply_drive():

    data = request.json

    student_id = data.get("student_id")
    drive_id = data.get("drive_id")
    notes = data.get("notes")

    result = apply_for_drive(db_session, student_id, drive_id, notes)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 400

    return jsonify(result), 201


@student_api.route("/<int:student_id>", methods=["PUT"])
@swag_from(update_student_swagger)
@role_required("STUDENT")
def update_student_profile(student_id):

    data = request.json

    result = update_student(db_session, student_id, data)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 404

    return jsonify(result), 200




@student_api.route("/<int:student_id>/applications", methods=["GET"])
@swag_from(get_student_applications_swagger)
@role_required("STUDENT")
def fetch_student_applications(student_id):

    result = get_student_applications(db_session, student_id)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 500

    return jsonify(result), 200

@student_api.route("/details/<int:student_id>", methods=["GET"])
@swag_from(get_student_details_swagger)
@role_required("STUDENT")
def fetch_student_details(student_id):

    result = get_student_by_id(db_session, student_id)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 404

    return jsonify(result), 200