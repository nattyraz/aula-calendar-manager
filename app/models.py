"""
Mod?les de donn?es SQLAlchemy
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Child(Base):
    __tablename__ = "children"
    
    id = Column(String, primary_key=True)
    name = Column(String(100), nullable=False)
    institution = Column(String(100))
    class_name = Column(String(50))
    google_calendar_id = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    events = relationship("Event", back_populates="child")
    assignments = relationship("Assignment", back_populates="child")

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    child_id = Column(String, ForeignKey("children.id"))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    location = Column(String(100))
    teacher = Column(String(100))
    subject = Column(String(100))
    event_type = Column(String(20))  # 'class', 'homework', 'message'
    google_event_id = Column(String(255))
    aula_event_id = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    child = relationship("Child", back_populates="events")

class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    child_id = Column(String, ForeignKey("children.id"))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    due_date = Column(DateTime)
    subject = Column(String(100))
    completed = Column(Boolean, default=False)
    google_event_id = Column(String(255))
    aula_assignment_id = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    child = relationship("Child", back_populates="assignments")

class SyncLog(Base):
    __tablename__ = "sync_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    child_id = Column(String, ForeignKey("children.id"))
    sync_type = Column(String(50))  # 'google_calendar', 'outlook', etc.
    status = Column(String(20))  # 'success', 'error', 'partial'
    message = Column(Text)
    synced_at = Column(DateTime, default=datetime.utcnow)