from pydantic import BaseModel
from typing import Optional


class DepartmentCreate(BaseModel):

    code: str
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True


class DepartmentResponse(BaseModel):

    id: int
    code: str
    name: str
    description: Optional[str]
    is_active: bool

    class Config:
        orm_mode = True

class FunctionalRoleMatrixCreate(BaseModel):
    email: str
    function: str
    role: str
    user_id: int

    currency: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None

    dept_codes: Optional[str] = None


class FunctionalRoleMatrixResponse(BaseModel):
    id: int
    email: str
    function: str
    role: str
    user_id: int

    currency: Optional[str]
    min_amount: Optional[float]
    max_amount: Optional[float]

    dept_codes: Optional[str]

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional


# ---------- APPROVER ----------

class ApproverCreate(BaseModel):
    username: str
    approver_level: int


class ApproverResponse(BaseModel):
    id: int
    approver_level: int
    username: str

    class Config:
        from_attributes = True


# ---------- BUDGET APPROVAL ----------

class BudgetApprovalCreate(BaseModel):
    approver_level: int   # user-friendly input
    currency: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None


class BudgetApprovalResponse(BaseModel):
    id: int
    approver_level: int
    currency: Optional[str]
    min_amount: Optional[float]
    max_amount: Optional[float]

    class Config:
        from_attributes = True