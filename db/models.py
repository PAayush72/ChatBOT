from sqlalchemy import BigInteger, Column, Integer, Text, DateTime
from sqlalchemy.sql import func
from db.session import Base

class ChatMemory(Base):
    __tablename__ = "chat_memory"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True)   # 🔥 FIX
    user_message = Column(Text)
    bot_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserFact(Base):
    __tablename__ = "user_facts"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True)   # 🔥 FIX
    key = Column(Text)
    value = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())