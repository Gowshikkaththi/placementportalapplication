from flask import Blueprint, jsonify,request
from flasgger import swag_from
from controller_impl.company_impl import *
from config.swagger import *
from config.db_creation import db_session
from config.decorators import role_required
from flask import Flask, render_template, request, redirect, url_for, session, flash

company_api = Blueprint("company_api", __name__)

@company_api.route("/dashboard/")
def company_dashboard():
    company_id = session.get('table_id')
    company = get_company_by_id(db_session, company_id)

    return render_template(
        "company_dashboard.html",
        company=company,
        company_id=company_id
    )

@company_api.route("/placement-drives", methods=["POST"])
@swag_from(create_placement_drive_swagger)
@role_required("COMPANY")
def create_drive():

    data = request.json

    drive = create_placement_drive(db_session,data)

    return jsonify({
        "id": drive.id,
        "company_id": drive.company_id,
        "job_title": drive.job_title,
        "status": drive.status.value
    }), 201


@company_api.route("/<int:company_id>/placement-drives", methods=["GET"])
@swag_from(get_drives_by_company_swagger)
@role_required("COMPANY")
def view_company_drives(company_id):

    drives = get_drives_by_company(db_session, company_id)

    result = []

    for drive in drives:
        result.append({
            "id": drive.id,
            "job_title": drive.job_title,
            "job_description": drive.job_description,
            "eligibility_criteria": drive.eligibility_criteria,
            "minimum_CGPA": drive.minimum_CGPA,
            "application_deadline": drive.application_deadline,
            "status": drive.status.value,
            "location": drive.location,
            "salary_package": drive.salary_package
        })

    return jsonify(result), 200



@company_api.route("/placement-drives/<int:drive_id>/applications", methods=["GET"])
@swag_from(get_applications_by_drive_swagger)
@role_required("COMPANY")
def view_applications_for_drive(drive_id):

    applications = get_applications_by_drive(db_session, drive_id)

    result = []

    for app in applications:
        result.append({
            "id": app.id,
            "student_id": app.student_id,
            "drive_id": app.drive_id,
            "application_date": app.application_date,
            "status": app.status.value,
            "notes": app.notes
        })

    return jsonify(result), 200


@company_api.route("/students/<int:student_id>", methods=["GET"])
@swag_from(get_student_by_id_swagger)
@role_required("COMPANY")
def view_student(student_id):

    student = get_student_by_id(db_session, student_id)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student), 200



@company_api.route("/applications/<int:application_id>/status", methods=["PUT"])
@swag_from(update_application_status_swagger)
@role_required("COMPANY")
def change_application_status(application_id):

    data = request.json
    status = data.get("status")

    result = update_application_status(db_session, application_id, status)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 404

    return jsonify({
        "id": result.id,
        "student_id": result.student_id,
        "drive_id": result.drive_id,
        "status": result.status.value
    }), 200



@company_api.route("/<int:company_id>", methods=["GET"])
@swag_from(get_company_by_id_swagger)
@role_required("COMPANY")
def fetch_company(company_id):
    result = get_company_by_id(db_session, company_id)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 404

    return jsonify(result), 200