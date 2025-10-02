from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, JSON
from sqlalchemy.sql.expression import text
from .database import Base
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    source_type = Column(String(50), nullable=False)  # "web" ou "pdf"
    title = Column(String(255), nullable=False)
    summary = Column(JSON, nullable=False)            # Résumé court/détaillé
    questions = Column(JSON, nullable=False)          # Liste Q/R
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))