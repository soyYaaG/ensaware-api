from datetime import datetime
from pydantic import BaseModel


class ProfileBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class Profile(ProfileBase):
    id: str
    is_active: bool
    created: datetime
    modified: datetime | None

    class Config:
        from_attributes = True
