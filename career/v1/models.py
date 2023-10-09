from sqlalchemy import Boolean, Column, String, TIMESTAMP, text

from utils import UTC, UUID_4
from utils.database import Base


class CareerModel(Base):
    __tablename__ = 'career'

    id = Column(String(60), primary_key=True,
                index=True, default=UUID_4)
    name = Column(String(100), index=True, unique=True)
    is_active = Column(Boolean, default=True)
    created = Column(TIMESTAMP, default=UTC)
    modified = Column(TIMESTAMP, default=None)
