from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean
from sqlalchemy.orm import declarative_base
import datetime as dt

Base = declarative_base()


class CompanyRecord(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    website = Column(String(500), nullable=True)
    industry = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    remote_ok = Column(Boolean, default=False)
    score = Column(Integer, default=0)
    source = Column(String(255), nullable=True)
    tags = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow)


class ProfileDocument(Base):
    __tablename__ = "profile_documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_name = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow)


class EmailDraftRecord(Base):
    __tablename__ = "email_drafts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255), nullable=False)
    subject = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)
    status = Column(String(100), default="draft")
    created_at = Column(DateTime, default=dt.datetime.utcnow)


class CycleRunRecord(Base):
    __tablename__ = "cycle_runs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_name = Column(String(255), nullable=False)
    focus_terms = Column(Text, nullable=False)
    artifact_dir = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
