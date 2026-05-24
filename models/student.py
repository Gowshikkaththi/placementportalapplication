from sqlalchemy import (
    Column, String, Integer, BigInteger, Date,
    Boolean, Numeric, ForeignKey, Text,
    TIMESTAMP, Index,Enum
)
from sqlalchemy.orm import  relationship
from sqlalchemy.sql import func
from config.db_creation import Base
import enum


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True,autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    roll_number = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(15), nullable=False)
    gender = Column(String(10))
    date_of_birth = Column(Date)

    department = Column(String(100), nullable=False)
    degree = Column(String(100), nullable=False)
    specialization = Column(String(100))
    batch_year = Column(Integer, nullable=False)

    cgpa = Column(Numeric(4, 2))
    tenth_percentage = Column(Numeric(5, 2))
    twelfth_percentage = Column(Numeric(5, 2))
    diploma_percentage = Column(Numeric(5, 2))

    active_backlogs = Column(Integer, default=0)
    total_backlogs = Column(Integer, default=0)

    placement_status = Column(String(30), default="NOT_PLACED")
    willing_to_relocate = Column(Boolean, default=True)

    github_url = Column(Text)
    linkedin_url = Column(Text,nullable= True)
    portfolio_url = Column(Text,nullable= True)
    leetcode_rating = Column(Integer,nullable= True)
    hackerrank_rating = Column(Integer,nullable= True)
    skills = Column(Text)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    #skills = relationship("StudentSkill", back_populates="student", cascade="all, delete-orphan")
    #documents = relationship("StudentDocument", back_populates="student", cascade="all, delete-orphan")
    #applications = relationship("StudentApplication", back_populates="student", cascade="all, delete-orphan")
    user = relationship("User", back_populates="student")

    __table_args__ = (
        Index("idx_students_batch", "batch_year"),
        Index("idx_students_status", "placement_status"),
    )



    def to_dict(self):
        data = {}

        for column in self.__table__.columns:
            value = getattr(self, column.name)

            if isinstance(value, enum.Enum):
                value = value.value

            data[column.name] = value

        return data