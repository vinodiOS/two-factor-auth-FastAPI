from database.base_class import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    secret = Column(String, nullable=False)