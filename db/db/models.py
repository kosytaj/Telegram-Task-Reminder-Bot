from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
import enum
import datetime

Base = declarative_base()

class TaskStatus(enum.Enum):
PENDING = "PENDING"
DONE = "DONE"
CANCELLED = "CANCELLED"
RESCHEDULED = "RESCHEDULED"

class User(Base):
tablename = "users"

id = Column(Integer, primary_key=True)
tg_id = Column(Integer, unique=True, nullable=False)
username = Column(String)
timezone = Column(String, default="UTC")
created_at = Column(DateTime, default=datetime.datetime.utcnow)
class Task(Base):
tablename = "tasks"

id = Column(Integer, primary_key=True)
title = Column(String, nullable=False)
creator_id = Column(Integer, ForeignKey("users.tg_id"), nullable=False)
assignee_id = Column(Integer, ForeignKey("users.tg_id"), nullable=False)
scheduled_at = Column(DateTime, nullable=False)
status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
created_at = Column(DateTime, default=datetime.datetime.utcnow)