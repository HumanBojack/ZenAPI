from sqlalchemy import MetaData, Table, Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

# metadata = MetaData()

# users = Table('users', metadata,
#   Column('first_name', String(100), nullable=False),
#   Column('last_name', String(100), nullable=False),
#   Column('username', String(100), nullable=False, unique=True),
#   Column('is_admin', Boolean(), server_default='f')
# )

Base = declarative_base()

class User(Base):
  __tablename__ = "users"
  username = Column(String(100), nullable=False, unique=True, primary_key=True)
  first_name = Column(String(100), nullable=False)
  last_name = Column(String(100), nullable=False)
  is_admin = Column(Boolean(), server_default='f')