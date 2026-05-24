from config.db_creation import db_session
from models.application import Application
from models.application import ApplicationStatus
from models.company import Company

def apply_for_drive(db_session: db_session, student_id, drive_id,notes:None):
    db = db_session()
    # 🔹 Check if student already applied
    existing_application = db.query(Application).filter(
        Application.student_id == student_id,
        Application.drive_id == drive_id
    ).first()

    if existing_application:
        return {"error": "Student already applied for this placement drive"}

    # 🔹 Create new application
    application = Application(
        student_id=student_id,
        drive_id=drive_id,
        status=ApplicationStatus.APPLIED,
        notes = notes
    )

    db.add(application)
    db.commit()
    db.refresh(application)
    db.close()
    return application.to_dict()



from models.student import Student


def update_student(db_session: db_session, student_id, data):
    db = db_session()
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        return {"error": "Student not found"}

    # Update fields dynamically
    for key, value in data.items():
        if hasattr(student, key):
            setattr(student, key, value)

    db.commit()
    db.refresh(student)
    db.close()
    return student.to_dict()



from models.placement_drive import PlacementDrive, DriveStatus


from sqlalchemy.orm import joinedload
from sqlalchemy import and_

def get_approved_drives(db_session, student_id):
    try:
        db = db_session()

        drives = (
            db.query(PlacementDrive)
            .join(Company)  # join company
            .outerjoin(
                Application,
                and_(
                    Application.drive_id == PlacementDrive.id,
                    Application.student_id == student_id
                )
            )
            .filter(
                PlacementDrive.status == DriveStatus.APPROVED,
                Application.id == None  # student has NOT applied
            )
            .all()
        )

        result = []

        for drive in drives:
            data = drive.to_dict()
            data["company_name"] = drive.company.company_name
            result.append(data)
        db.close()
        return result

    except Exception as e:
        return {"error": str(e)}



from models.application import Application
from models.placement_drive import PlacementDrive


def get_student_applications(db_session: db_session, student_id: int):
    try:
        db = db_session()
        applications = (
            db.query(Application)
            .join(Application.drive)
            .filter(Application.student_id == student_id)
            .all()
        )

        result = []

        for app in applications:
            drive = app.drive

            result.append({
                "application_id": app.id,
                "application_date": app.application_date,
                "application_status": app.status.value,

                "drive": {
                    "drive_id": drive.id,
                    "job_title": drive.job_title,
                    "company_name": drive.company.company_name if drive.company else None,
                    "location": drive.location,
                    "salary_package": drive.salary_package,
                    "application_deadline": drive.application_deadline
                },

                "notes": app.notes
            })
        db.close()
        return result

    except Exception as e:
        return {"error": str(e)}

def get_student_by_id(db_session: db_session, student_id: int):
    db = db_session()
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        return {"error": "Student not found"}
    db.close()
    return {
        "id": student.id,
        "user_id": student.user_id,
        "roll_number": student.roll_number,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "email": student.email,
        "phone": student.phone,
        "gender": student.gender,
        "date_of_birth": student.date_of_birth,
        "department": student.department,
        "degree": student.degree,
        "specialization": student.specialization,
        "batch_year": student.batch_year,
        "cgpa": float(student.cgpa) if student.cgpa else None,
        "tenth_percentage": float(student.tenth_percentage) if student.tenth_percentage else None,
        "twelfth_percentage": float(student.twelfth_percentage) if student.twelfth_percentage else None,
        "diploma_percentage": float(student.diploma_percentage) if student.diploma_percentage else None,
        "active_backlogs": student.active_backlogs,
        "total_backlogs": student.total_backlogs,
        "placement_status": student.placement_status,
        "willing_to_relocate": student.willing_to_relocate,
        "github_url": student.github_url,
        "linkedin_url": student.linkedin_url,
        "portfolio_url": student.portfolio_url,
        "leetcode_rating": student.leetcode_rating,
        "hackerrank_rating": student.hackerrank_rating,
        "skills": student.skills,
        "created_at": student.created_at,
        "updated_at": student.updated_at
    }


