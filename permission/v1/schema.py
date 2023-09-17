from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

from profile.v1.schema import Profile


class ContentTypeBase(BaseModel):
    model: str

    class Config:
        from_attributes = True


class ContentType(ContentTypeBase):
    id: UUID
    created: datetime
    modified: datetime | None

    class Config:
        from_attributes = True


class PermissionBase(BaseModel):
    content_type_id: UUID
    code_name: str
    description: str

    class Config:
        from_attributes = True


class Permission(PermissionBase):
    id: UUID
    created: datetime
    modified: datetime | None

    class Config:
        from_attributes = True


class PermissionProfileBase(BaseModel):
    permission_id: UUID
    profile_id: UUID

    class Config:
        from_attributes = True


class PermissionProfile(PermissionProfileBase):
    id: UUID
    created: datetime
    modified: datetime | None

    class Config:
        from_attributes = True


class ReadPermissionProfile(BaseModel):
    id: UUID
    permission: Permission
    profile: Profile
    created: datetime
    modified: datetime | None

    class Config:
        from_attributes = True
