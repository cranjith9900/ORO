from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from .schemas import UserCreate, UserResponse
from .controller import create_user, get_users, get_user_by_id
from .schemas import GroupCreate, GroupResponse
from .controller import create_group
router = APIRouter(prefix="/users", tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UserResponse)
def add_user(data: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, data)


@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return get_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id(db, user_id)

@router.post("/groups", response_model=GroupResponse)
def add_group(data: GroupCreate, db: Session = Depends(get_db)):
    return create_group(db, data)

@router.get("/groups", response_model=list[GroupResponse])
def list_groups(db: Session = Depends(get_db)):
    return get_groups(db)