from models.student import Student
from models.company import Company
from models.company_user import CompanyUser
from models.placement_drive import PlacementDrive
from models.application import Application

from config.db_creation import engine,Base
import traceback


def create_db_and_tables():
    try:
        conn = engine.connect()
        print("Database created!")
        Base.metadata.create_all(engine)
        print("Tables created!")

    except Exception as e:
        print("Error occured !!!")
        traceback.print_exc()