from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///user.db', echo=True)
Base = declarative_base()


class Application(Base):
    __tablename__ = "application"

    name = Column(String, primary_key=True)

    def __init__(self, name):
        self.name = name


Base.metadata.create_all(engine)



