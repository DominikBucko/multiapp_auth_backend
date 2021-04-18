from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///user.db', echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    email = Column(String, primary_key=True)
    password = Column(String)

    def __init__(self, email, password):
        self.email = email
        self.password = password


Base.metadata.create_all(engine)
