from flask_security import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, DateTime,Enum
from sqlalchemy.orm import relationship
from config.db_creation import Base
from datetime import datetime
from models.user_role import roles_users
import enum

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(255), unique=True)

    password = Column(String(255), nullable=False)

    active = Column(Boolean(), default=True)
    approved_status = Column(String(255), nullable=False)

    # 🔹 auditing fields
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)

    approved_at = Column(DateTime, nullable=True)
    approved_by = Column(Integer, nullable=True)

    roles = relationship(
        "Role",
        secondary=roles_users,
        backref="users"
    )
    student = relationship(
        "Student",
        back_populates="user",
        uselist=False
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
