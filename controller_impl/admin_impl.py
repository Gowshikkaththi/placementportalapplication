from config.constants import roles, admin_role,company_role,description,student_role
from flask import abort,jsonify,request
from models.users import User
from models.roles import Role
from models.user_role import roles_users
from models.student import Student
from werkzeug.security import generate_password_hash
from datetime import datetime
from config.db_creation import db_session
from models.company import Company,ApprovalStatus
from models.application import Application
from models.company_user import CompanyUser
from config.db_creation import engine
import traceback
from models.placement_drive import PlacementDrive
from models.placement_drive import DriveStatus


def view_unapproved_user():
    db = db_session()
    users = db.query(User).filter(
        User.approved_status == "Pending"
    ).all()
    db.close()
    return [user.to_dict() for user in users]

def update_user_approval(db_session: db_session, user_id, status, admin_id):
    db = db_session()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}
    user.approved_status = status
    user.approved_at = datetime.utcnow()
    user.approved_by = admin_id
    db.commit()
    db.refresh(user)
    db.close()
    return user.to_dict()


def get_pending_companies(db_session: db_session):
    db = db_session()
    companies = db.query(Company).filter(
        Company.approval_status == ApprovalStatus.PENDING
    ).all()
    db.close()
    return [company.to_dict() for company in companies]

def update_company_approval(db_session: db_session, company_id, status):
    db = db_session()
    company = db.query(Company).filter(
        Company.id == company_id
    ).first()
    if not company:
        return {"error": "Company not found"}
    company.approval_status = status
    company.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(company)
    db.close()
    return company.to_dict()



def get_all_applications(db_session: db_session):
    db = db_session()
    applications = db.query(Application).all()
    db.close()
    return [application.to_dict() for application in applications]


def get_all_placement_drives(db_session: db_session):
    db = db_session()
    drives = db.query(PlacementDrive).all()
    db.close()
    return [drive.to_dict() for drive in drives]



def get_pending_placement_drives(db_session: db_session):
    db = db_session()

    drives = (
        db.query(PlacementDrive, Company)
        .join(Company, PlacementDrive.company_id == Company.id)
        .filter(PlacementDrive.status == DriveStatus.PENDING)
        .all()
    )

    result = []

    for drive, company in drives:
        data = drive.to_dict()
        data["company_name"] = company.company_name
        data["website"] = company.website
        result.append(data)
    db.close()
    return result


def update_drive_status(db_session: db_session, drive_id, status):
    db = db_session()
    drive = db.query(PlacementDrive).filter(
        PlacementDrive.id == drive_id
    ).first()
    if not drive:
        return {"error": "Placement drive not found"}
    drive.status = status
    db.commit()
    db.refresh(drive)
    db.close()
    return drive.to_dict()

def get_admin_by_id(db_session: db_session, user_id: int):
    db = db_session()
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {"error": "User not found"}

    # Check if user has ADMIN role
    is_admin = any(role.name == "ADMIN" for role in user.roles)
    if not is_admin:
        return {"error": "User is not an admin"}
    db.close()
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "active": user.active,
        "approved_status": user.approved_status,
        "created_at": user.created_at,
        "created_by": user.created_by,
        "approved_at": user.approved_at,
        "approved_by": user.approved_by,
        "roles": [role.name for role in user.roles]
    }

