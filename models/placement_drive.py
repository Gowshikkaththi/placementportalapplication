from sqlalchemy import (
    Column, String, Integer, BigInteger, Text,
    ForeignKey, DateTime, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from config.db_creation import Base


class DriveStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    CLOSED = "CLOSED"
    REJECTED = "REJECTED"

class PlacementDrive(Base):
    __tablename__ = "placement_drives"

    id = Column(Integer, primary_key=True,autoincrement=True)

    company_id = Column(
        BigInteger,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False
    )

    job_title = Column(String(200), nullable=False)
    job_description = Column(Text)

    eligibility_criteria = Column(Text)
    minimum_CGPA = Column(Text)
    application_deadline = Column(DateTime)

    status = Column(
        Enum(DriveStatus),
        default=DriveStatus.PENDING
    )

    location = Column(String(200))
    salary_package = Column(String(100))

    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    company = relationship("Company", back_populates="placement_drives")

    applications = relationship(
        "Application",
        back_populates="drive",
        cascade="all, delete-orphan"
    )

    import enum

    def to_dict(self):
        data = {}

        for column in self.__table__.columns:
            value = getattr(self, column.name)

            if isinstance(value, enum.Enum):
                value = value.value

            data[column.name] = value

        return data