from datetime import datetime
from pydantic import BaseModel


class DomainBase(BaseModel):
    value: str

    class Config:
        from_attributes = True


class Domain(DomainBase):
    id: str
    created: datetime
    modified: datetime | None

    class Config:
        from_attributes = True
