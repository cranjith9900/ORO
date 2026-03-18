from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from pydantic import BaseModel
# Association table (Many-to-Many)
user_group_association = Table(
    "user_groups",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("group_id", Integer, ForeignKey("groups.id")),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    realm_id = Column(String, nullable=True)

    groups = relationship(
        "Group",
        secondary=user_group_association,
        back_populates="users"
    )


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship(
        "User",
        secondary=user_group_association,
        back_populates="groups"
    )

class GroupCreate(BaseModel):
    name: str


class GroupResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True