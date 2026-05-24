from sqlalchemy import (
    Column, String, Integer, BigInteger, Text,
    ForeignKey, DateTime, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from config.db_creation import Base

class ApprovalStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True,autoincrement=True)
    company_name = Column(String(255), nullable=False, unique=True)
    website = Column(String(255))

    approval_status = Column(
        Enum(ApprovalStatus),
        default=ApprovalStatus.PENDING
    )

    description = Column(Text)
    industry = Column(String(150))
    headquarters = Column(String(200))

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    placement_drives = relationship(
        "PlacementDrive",
        back_populates="company",
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