import datetime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey


Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversation'
    