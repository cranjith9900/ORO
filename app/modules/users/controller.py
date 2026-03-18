from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from .models import Group,User
from sqlalchemy.orm import Session



def create_user(db: Session, data):

    # 1. Extract group_ids separately
    group_ids = data.group_ids

    # 2. Fetch groups from DB
    groups = db.query(Group).filter(
        Group.id.in_(group_ids)
    ).all()

    # Optional validation
    if len(groups) != len(group_ids):
        raise HTTPException(
            status_code=400,
            detail="Some groups not found"
        )

    # 3. Create user WITHOUT group_ids
    user = User(
        username=data.username,
        role=data.role,
        realm_id=data.realm_id,
        groups=groups   # ✅ assign relationship
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
        
def get_users(db: Session):
    return db.query(User).all()
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_group(db: Session, data):

    # check duplicate group name
    existing = db.query(Group).filter(
        Group.name == data.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Group already exists"
        )

    group = Group(name=data.name)

    try:
        db.add(group)
        db.commit()
        db.refresh(group)
        return group

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error creating group"
        )

def get_groups(db: Session):
    return db.query(Group).all()