from config.constants import roles, admin_role, company_role, student_role
from flask import abort, jsonify
from models.users import User
from models.roles import Role
from models.user_role import roles_users
from models.student import Student
from models.company import Company, ApprovalStatus
from models.company_user import CompanyUser
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import Session
from config.db_creation import engine
import traceback


def register_user(data):

    if data['role'] not in roles:
        abort(400, description="Role does not exist")

    if data['role'] == admin_role:
        abort(400, description="Admin cannot register")

    session = Session(engine)

    try:

        # ---------- ROLE ----------
        role_entry = session.query(Role).filter_by(
            name=data["role"]
        ).first()

        if not role_entry:
            abort(400, description="Role not found")

        # ---------- USER EXISTS CHECK ----------
        existing_user = session.query(User).filter_by(
            username=data["username"]
        ).first()

        if existing_user:
            abort(400, description="User already exists")

        # ---------- APPROVAL STATUS ----------
        approved_status = "Approved"
        if data["role"] == company_role:
            approved_status = "Pending"

        # ---------- CREATE USER ----------
        user = User(
            username=data["username"],
            email=data["email"],
            password=generate_password_hash(data["password"]),
            active=True,
            approved_status=approved_status,
            created_by="SYSTEM"
        )

        session.add(user)
        session.flush()

        # ---------- ASSIGN ROLE ----------
        user.roles.append(role_entry)

        # ---------- ROLE SPECIFIC REGISTRATION ----------
        if data["role"] == student_role:
            response = register_student(session, user, data)

        elif data["role"] == company_role:
            response = register_company(session, user, data)

        else:
            response = {"message": "User created successfully"}

        session.commit()

        return response

    except Exception as e:
        session.rollback()
        print(traceback.format_exc())
        abort(500, description="Error creating user")

    finally:
        session.close()


# ---------------------------------------------------
# STUDENT REGISTRATION
# ---------------------------------------------------

def register_student(session, user, data):

    existing_student = session.query(Student).filter_by(
        user_id=user.id
    ).first()

    if existing_student:
        return jsonify({
            "error": "Student profile already exists"
        }), 400

    student = Student(

        user_id=user.id,

        roll_number=data["roll_number"],
        first_name=data["first_name"],
        last_name=data.get("last_name"),

        email=data["email"],
        phone=data["phone"],
        gender=data.get("gender"),
        date_of_birth=data.get("date_of_birth"),

        department=data["department"],
        degree=data["degree"],
        specialization=data.get("specialization"),
        batch_year=data["batch_year"],

        cgpa=data.get("cgpa"),
        tenth_percentage=data.get("tenth_percentage"),
        twelfth_percentage=data.get("twelfth_percentage"),
        diploma_percentage=data.get("diploma_percentage"),

        active_backlogs=data.get("active_backlogs", 0),
        total_backlogs=data.get("total_backlogs", 0),

        placement_status="NOT_PLACED",

        willing_to_relocate=data.get("willing_to_relocate", True),

        github_url=data.get("github_url"),
        linkedin_url=data.get("linkedin_url"),
        portfolio_url=data.get("portfolio_url"),

        leetcode_rating=data.get("leetcode_rating"),
        hackerrank_rating=data.get("hackerrank_rating"),

        skills=data.get("skills")
    )

    session.add(student)

    return jsonify({
        "message": "Student registered successfully",
        "user_id": user.id
    }), 201


# ---------------------------------------------------
# COMPANY REGISTRATION
# ---------------------------------------------------

def register_company(session, user, data):

    company = session.query(Company).filter_by(
        company_name=data["company_name"]
    ).first()

    # ---------- CREATE COMPANY ----------
    if not company:

        company = Company(
            company_name=data["company_name"],
            website=data.get("website"),
            industry=data.get("industry"),
            headquarters=data.get("headquarters"),
            description=data.get("description"),
            approval_status=ApprovalStatus.PENDING
        )

        session.add(company)
        session.flush()

    # ---------- CHECK MAPPING ----------
    existing_mapping = session.query(CompanyUser).filter_by(
        user_id=user.id,
        company_id=company.id
    ).first()

    if existing_mapping:
        return jsonify({
            "message": "User already mapped to this company"
        }), 400

    # ---------- CREATE MAPPING ----------
    company_user = CompanyUser(
        user_id=user.id,
        company_id=company.id
    )

    session.add(company_user)

    return jsonify({
        "message": "Company registered. Pending admin approval",
        "user_id": user.id,
        "company_id": company.id
    }), 201