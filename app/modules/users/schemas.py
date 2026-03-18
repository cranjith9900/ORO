from pydantic import BaseModel
from typing import List, Optional


class GroupResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    role: str
    realm_id: Optional[str] = None
    group_ids: List[int] = []


class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    realm_id: Optional[str]
    groups: List[GroupResponse]

    class Config:
        from_attributes = True

from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str


class GroupResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True