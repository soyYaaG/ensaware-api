from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class ProfileBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class Profile(ProfileBase):
    id: UUID
    is_active: bool
    created: datetime
    modified: datetime | None

    class Config:
        from_attributes = True
