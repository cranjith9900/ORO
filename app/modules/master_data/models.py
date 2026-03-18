from sqlalchemy import Column, Integer, String, Float, ForeignKey,Boolean
from app.database import Base
from sqlalchemy.orm import relationship


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class FunctionalRoleMatrix(Base):
    __tablename__ = "functional_role_matrix"

    id = Column(Integer, primary_key=True)

    email = Column(String, nullable=False)
    function = Column(String, nullable=False)
    role = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    currency = Column(String, nullable=True)

    min_amount = Column(Float, nullable=True)
    max_amount = Column(Float, nullable=True)

    dept_codes = Column(String, nullable=True)  # can store CSV or JSON later

    # Relationship
    user = relationship("User")



class Approver(Base):
    __tablename__ = "approvers"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approver_level = Column(Integer, nullable=False)

    user = relationship("User")


class BudgetApproval(Base):
    __tablename__ = "budget_approvals"

    id = Column(Integer, primary_key=True)

    approver_id = Column(Integer, ForeignKey("approvers.id"), nullable=False)

    currency = Column(String, nullable=True)

    min_amount = Column(Float, nullable=True)
    max_amount = Column(Float, nullable=True)

    approver = relationship("Approver")