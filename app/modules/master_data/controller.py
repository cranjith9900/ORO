from sqlalchemy.orm import Session
from .models import Department


from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from .models import FunctionalRoleMatrix
from app.modules.users.models import User

from .models import Approver, BudgetApproval
from app.modules.users.models import User

def create_department(db: Session, data):

    dept = Department(**data.model_dump(exclude_unset=True))

    try:
        db.add(dept)
        db.commit()
        db.refresh(dept)
        return dept

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Department with this code already exists"
        )

def get_departments(db: Session):

    return db.query(Department).all()


def get_active_departments(db: Session):

    return db.query(Department).filter(
        Department.is_active == True
    ).all()

def create_functional_role(db: Session, data):

    # check user exists
    user = db.query(User).filter(User.id == data.user_id).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )

    obj = FunctionalRoleMatrix(**data.model_dump(exclude_unset=True))

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj

def create_approver(db: Session, data):

    # find user by username
    user = db.query(User).filter(
        User.username == data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )

    approver = Approver(
        user_id=user.id,
        approver_level=data.approver_level
    )

    db.add(approver)
    db.commit()
    db.refresh(approver)

    return approver

def get_approvers(db: Session):
    return db.query(Approver).all()

def create_budget_rule(db: Session, data):

    # find approver by level
    approver = db.query(Approver).filter(
        Approver.approver_level == data.approver_level
    ).first()

    if not approver:
        raise HTTPException(
            status_code=400,
            detail="Approver level not found"
        )

    rule = BudgetApproval(
        approver_id=approver.id,
        currency=data.currency,
        min_amount=data.min_amount,
        max_amount=data.max_amount
    )

    db.add(rule)
    db.commit()
    db.refresh(rule)

    return rule

def get_budget_rules(db: Session):
    return db.query(BudgetApproval).all()

def get_approver_for_amount(db: Session, amount, currency):

    rule = db.query(BudgetApproval).filter(
        BudgetApproval.min_amount <= amount,
        BudgetApproval.max_amount >= amount,
        BudgetApproval.currency == currency
    ).first()

    if not rule:
        raise HTTPException(
            status_code=404,
            detail="No approval rule found"
        )

    return rule.approver.user