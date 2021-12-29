import datetime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from flaskbb.user.models import User


Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversation'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    tag = Column(String)
    conversation_start_time = Column(DateTime)
    user_id = Column(Integer)
    Message = relationship("Message", backref="conversation")



class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    messageTime = Column(DateTime)
    conversationId = Column(Integer, ForeignKey('conversation.id'))





