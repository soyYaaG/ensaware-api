from sqlalchemy import Boolean, Column, String, TIMESTAMP

from utils.database import Base
from utils.settings import DefaultValuesModels


class CareerModel(Base):
    __tablename__ = 'career'

    id = Column(String(60), primary_key=True,
                index=True, default=DefaultValuesModels.uuid4())
    name = Column(String(100), index=True, unique=True)
    is_active = Column(Boolean, default=True)
    created = Column(TIMESTAMP, default=DefaultValuesModels.utc())
    modified = Column(TIMESTAMP, default=None)
