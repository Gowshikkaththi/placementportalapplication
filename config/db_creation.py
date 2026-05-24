from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import traceback

Base = declarative_base()
engine = create_engine("sqlite:///placement23f1002989.db",echo=True)
db_session = sessionmaker(bind=engine)