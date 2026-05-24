from flask_security import RoleMixin
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.db_creation import Base

class Role(Base, RoleMixin):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String)