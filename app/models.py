import uuid
from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Domain(Base):
    __tablename__ = 'domains'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    scans = relationship("Scan", back_populates="domain")


class Scan(Base):
    __tablename__ = 'scans'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    domain_id = Column(UUID(as_uuid=True), ForeignKey('domains.id'), nullable=False)
    data = Column(JSON, nullable=False)
    status = Column(String, nullable=False)

    domain = relationship("Domain", back_populates="scans")
