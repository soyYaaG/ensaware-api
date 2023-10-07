from sqlalchemy import Boolean, Column, ForeignKey, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

from career.v1.models import CareerModel
from profiles.v1.models import ProfileModel
from utils import UTC
from utils.database import Base


class UserModel(Base):
    __tablename__ = 'user'

    id = Column(String(60), primary_key=True,
                index=True, server_default=text('UUID()'))
    provider_id = Column(String(60), unique=True, index=True)
    provider = Column(String(50), nullable=False, index=True)
    display_name = Column(String(255), nullable=False)
    email = Column(String(100), index=True, unique=True)
    picture = Column(String(255), nullable=True)
    profile_id = Column(String(60), ForeignKey(
        'profile.id'), nullable=False)
    career_id = Column(String(60), ForeignKey(
        'career.id'), nullable=True)
    refresh_token = Column(String(255), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created = Column(TIMESTAMP, default=UTC)
    modified = Column(TIMESTAMP, default=None)

    profile = relationship('ProfileModel')
    career = relationship('CareerModel')
