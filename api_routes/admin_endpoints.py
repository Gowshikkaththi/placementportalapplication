from flask import Blueprint, jsonify,request
from flasgger import swag_from
from controller_impl.admin_impl import *
from config.swagger import *
from config.db_creation import db_session
from config.decorators import role_required
from flask import Flask, render_template, request, redirect, url_for, session, flash

admin_api = Blueprint("admin_api", __name__)

from flask import jsonify
from flasgger import swag_from

@admin_api.route("/admin/dashboard")
def admin_dashboard():
    # Ensure session and role check
    if "roles" not in session or "ADMIN" not in session["roles"]:
        flash("Access denied!", "danger")
        return redirect(url_for("login"))

    # Fetch data from your existing controller functions
    students = view_unapproved_user()  # returns list of dicts
    companies = get_pending_companies(db_session)
    drives = get_pending_placement_drives(db_session)



    return render_template(
        "admin_dashboard.html",
        admin_name=session.get("username", "Admin"),
        admin_id=session.get("user_id"),
        students=students,
        companies=companies,
        drives=drives
    )

@admin_api.route("/unapproved-users", methods=["GET"])
@swag_from(view_unapproved_users_swagger)
@role_required("ADMIN")
def get_unapproved_users():
    return jsonify(view_unapproved_user()),200



@admin_api.route("/users/<int:user_id>/approval", methods=["PUT"])
@swag_from(update_user_approval_swagger)
@role_required("ADMIN")
def approve_user(user_id):

    data = request.json
    status = data.get("status")
    admin_id = data.get("admin_id")

    result = update_user_approval(db_session, user_id, status, admin_id)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 404

    return jsonify(result), 200


@admin_api.route("/pending-companies", methods=["GET"])
@swag_from(get_pending_companies_swagger)
@role_required("ADMIN")
def view_pending_companies():

    companies = get_pending_companies(db_session)

    result = []

    for company in companies:
        result.append({
            "id": company.id,
            "company_name": company.company_name,
            "hr_contact_name": company.hr_contact_name,
            "hr_contact_email": company.hr_contact_email,
            "hr_contact_phone": company.hr_contact_phone,
            "website": company.website,
            "approval_status": company.approval_status.value
        })

    return jsonify(result), 200




@admin_api.route("/companies/<int:company_id>/approval", methods=["PUT"])
@swag_from(update_company_approval_swagger)
@role_required("ADMIN")
def approve_company(company_id):

    data = request.json
    status = data.get("status")

    result = update_company_approval(db_session, company_id, status)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 404

    return jsonify(result), 200




@admin_api.route("/applications", methods=["GET"])
@swag_from(get_all_applications_swagger)
@role_required("ADMIN")
def view_all_applications():

    applications = get_all_applications(db_session)
    return jsonify(applications), 200



@admin_api.route("/placement-drives", methods=["GET"])
@swag_from(get_all_placement_drives_swagger)
@role_required("ADMIN")
def view_all_placement_drives():

    drives = get_all_placement_drives(db_session)
    return jsonify(drives), 200



@admin_api.route("/placement-drives/pending", methods=["GET"])
@swag_from(get_pending_placement_drives_swagger)
@role_required("ADMIN")
def view_pending_placement_drives():

    drives = get_pending_placement_drives(db_session)

    return jsonify(drives), 200


@admin_api.route("/placement-drives/<int:drive_id>/status", methods=["PUT"])
@swag_from(update_drive_status_swagger)
@role_required("ADMIN")
def approve_placement_drive(drive_id):

    data = request.json
    status = data.get("status")

    result = update_drive_status(db_session, drive_id, status)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 404

    return jsonify(result), 200



@admin_api.route("/admin/<int:user_id>", methods=["GET"])
@swag_from(get_admin_by_id_swagger)
@role_required("ADMIN")
def fetch_admin_details(user_id):

    result = get_admin_by_id(db_session, user_id)

    if isinstance(result, dict) and "error" in result:
        if result["error"] == "User not found":
            return jsonify(result), 404
        else:
            return jsonify(result), 400

    return jsonify(result), 200

# Students
@admin_api.route("/users/<int:user_id>/approve/<status>")
def approve_user_route(user_id, status):
    result = update_user_approval(db_session, user_id, status, session["user_id"])
    if "error" in result:
        flash(result["error"], "danger")
    else:
        flash(f"Student {status.lower()} successfully", "success")
    return redirect(url_for("admin_api.admin_dashboard"))

# Companies
@admin_api.route("/companies/<int:company_id>/approve/<status>")
def approve_company_route(company_id, status):
    result = update_company_approval(db_session, company_id, status)
    if "error" in result:
        flash(result["error"], "danger")
    else:
        flash(f"Company {status.lower()} successfully", "success")
    return redirect(url_for("admin_api.admin_dashboard"))

# Placement Drives
@admin_api.route("/drives/<int:drive_id>/approve/<status>")
def approve_drive_route(drive_id, status):
    result = update_drive_status(db_session, drive_id, status)
    if "error" in result:
        flash(result["error"], "danger")
    else:
        flash(f"Drive {status.lower()} successfully", "success")
    return redirect(url_for("admin_api.admin_dashboard"))