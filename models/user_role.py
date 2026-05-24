from sqlalchemy import Table, Column, Integer, ForeignKey
from config.db_creation import Base
roles_users = Table(
    "roles_users",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role_id", Integer, ForeignKey("roles.id"))
)
