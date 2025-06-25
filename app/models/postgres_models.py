from sqlalchemy import Column, String, DateTime, Text
from app.db.postgres import Base
from datetime import datetime

class Agent(Base):
    __tablename__ = "agents"
    agent_id = Column(String, primary_key=True, index=True)
    os = Column(String)
    registered_at = Column(DateTime, default=datetime.utcnow)

class Command(Base):
    __tablename__ = "commands"
    id = Column(String, primary_key=True)
    agent_id = Column(String, index=True)
    command = Column(String)
    status = Column(String, default="pending")
    executed_at = Column(DateTime, nullable=True)
    output = Column(Text, nullable=True)
