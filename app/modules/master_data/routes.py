from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from .schemas import DepartmentCreate, DepartmentResponse , FunctionalRoleMatrixCreate, FunctionalRoleMatrixResponse
from .controller import create_department, get_departments, get_active_departments, create_functional_role
from .schemas import (
    ApproverCreate,
    ApproverResponse,
    BudgetApprovalCreate,
    BudgetApprovalResponse
)

from .controller import (
    create_approver,
    get_approvers,
    create_budget_rule,
    get_budget_rules,
    get_approver_for_amount
)
router = APIRouter(prefix="/departments", tags=["Departments"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=DepartmentResponse)
def add_department(data: DepartmentCreate, db: Session = Depends(get_db)):

    return create_department(db, data)


@router.get("/", response_model=list[DepartmentResponse])
def list_departments(db: Session = Depends(get_db)):

    return get_departments(db)


@router.get("/active", response_model=list[DepartmentResponse])
def list_active_departments(db: Session = Depends(get_db)):

    return get_active_departments(db)

@router.post("/functionalRoles", response_model=FunctionalRoleMatrixResponse)
def create_role(data: FunctionalRoleMatrixCreate, db: Session = Depends(get_db)):
    return create_functional_role(db, data)

# ---------------- APPROVER ---------------- #

@router.post("/approver", response_model=ApproverResponse)
def add_approver(data: ApproverCreate, db: Session = Depends(get_db)):
    return create_approver(db, data)


@router.get("/approver", response_model=list[ApproverResponse])
def list_approvers(db: Session = Depends(get_db)):
    return get_approvers(db)


# ---------------- BUDGET RULE ---------------- #

@router.post("/budget", response_model=BudgetApprovalResponse)
def add_budget_rule(data: BudgetApprovalCreate, db: Session = Depends(get_db)):
    return create_budget_rule(db, data)


@router.get("/budget", response_model=list[BudgetApprovalResponse])
def list_budget_rules(db: Session = Depends(get_db)):
    return get_budget_rules(db)


# ---------------- CORE API (IMPORTANT) ---------------- #

@router.get("/check")
def check_approver(amount: float, currency: str, db: Session = Depends(get_db)):
    user = get_approver_for_amount(db, amount, currency)

    return {
        "approver": user.username,
        "user_id": user.id
    }