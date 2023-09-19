from sqlalchemy import Boolean, Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID

from utils import UTC, UUID_4
from utils.database import Base


class CareerModel(Base):
    __tablename__ = 'career'

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=UUID_4)
    name = Column(String(100), index=True, unique=True)
    is_active = Column(Boolean, default=True)
    created = Column(TIMESTAMP, default=UTC)
    modified = Column(TIMESTAMP, default=None)
