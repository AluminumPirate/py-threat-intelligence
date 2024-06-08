import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Domain(Base):
    __tablename__ = 'domains'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    scans = relationship("Scan", back_populates="domain")


class Scan(Base):
    __tablename__ = 'scans'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    domain_id = Column(UUID(as_uuid=True), ForeignKey('domains.id'), nullable=False)
    data = Column(JSON, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    domain = relationship("Domain", back_populates="scans")
