from config.db_creation import db_session
from datetime import datetime
from models.placement_drive import PlacementDrive
from models.application import Application
from models.student import Student
from models.company import Company
from datetime import datetime

def create_placement_drive(db_session: db_session, data):
    db = db_session()
    drive = PlacementDrive(
        company_id=data["company_id"],
        job_title=data["job_title"],
        job_description=data.get("job_description"),
        eligibility_criteria=data.get("eligibility_criteria"),
        minimum_CGPA=data.get("minimum_CGPA"),
        application_deadline=datetime.strptime(data.get("application_deadline"), "%Y-%m-%d"),
        location=data.get("location"),
        salary_package=data.get("salary_package")
    )

    db.add(drive)
    db.commit()
    db.refresh(drive)
    db.close()
    return drive



def get_drives_by_company(db_session: db_session, company_id):
    db = db_session()
    drives = db.query(PlacementDrive).filter(
        PlacementDrive.company_id == company_id
    ).all()
    db.close()
    return drives



def get_applications_by_drive(db_session: db_session, drive_id):
    db = db_session()
    applications = db.query(Application).filter(
        Application.drive_id == drive_id
    ).all()
    db.close()
    return applications



def get_student_by_id(db_session: db_session, student_id):
    db = db_session()
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()
    db.close()
    return student.to_dict()


def update_application_status(db_session: db_session, application_id, status):
    db = db_session()
    application = db.query(Application).filter(
        Application.id == application_id
    ).first()

    if not application:
        return {"error": "Application not found"}

    application.status = status

    db.commit()
    db.refresh(application)
    db.close()
    return application

def get_company_by_id(db_session: db_session, company_id: int):
    db = db_session()
    company = db.query(Company).filter(Company.id == company_id).first()

    if not company:
        return {"error": "Company not found"}
    db.close()
    return {
        "id": company.id,
        "company_name": company.company_name,
        "website": company.website,
        "approval_status": company.approval_status.value,
        "description": company.description,
        "industry": company.industry,
        "headquarters": company.headquarters,
        "created_at": company.created_at,
        "updated_at": company.updated_at
    }