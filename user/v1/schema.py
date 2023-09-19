from datetime import datetime
from pydantic import BaseModel, EmailStr
from uuid import UUID

from career.v1.schema import Career
from profiles.v1.schema import Profile


class UserBase(BaseModel):
    provider_id: str
    provider: str
    display_name: str
    email: EmailStr
    picture: str | None
    profile_id: UUID
    refresh_token: str

    class Config:
        from_attributes = True


class User(UserBase):
    id: UUID
    career_id: UUID | None
    is_active: bool
    created: datetime
    modified: datetime | None

    class Config:
        from_attributes = True


class UserRead(BaseModel):
    career: Career | None
    created: datetime
    display_name: str
    email: EmailStr
    id: UUID
    is_active: bool
    modified: datetime | None
    provider_id: str
    provider: str
    picture: str | None
    profile: Profile | None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    career_id: str | None
