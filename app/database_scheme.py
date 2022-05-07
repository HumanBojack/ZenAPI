from sqlalchemy import MetaData, Table, Column, String, Boolean, Text, Integer, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

# metadata = MetaData()

# users = Table('users', metadata,
#   Column('first_name', String(100), nullable=False),
#   Column('last_name', String(100), nullable=False),
#   Column('username', String(100), nullable=False, unique=True),
#   Column('is_admin', Boolean(), server_default='f')
# )

Base = declarative_base()

class User(Base):
  __tablename__ = "user"
  username = Column(String(100), nullable=False, unique=True, primary_key=True)
  first_name = Column(String(100), nullable=False)
  last_name = Column(String(100), nullable=False)
  is_admin = Column(Boolean(), server_default='f')

class DailyText(Base):
  __tablename__ = "dailytext"
  id = Column(Integer, primary_key=True, unique=True)
  text = Column(Text(), nullable=False)
  date = Column(Date(), server_default=func.now())
  emotion = Column(String(100), nullable=True)
  user_username = Column(ForeignKey("user.username", ondelete='CASCADE'), nullable=False)

  user = relationship("User", backref=backref("dailytext", passive_deletes=True))
