from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from server_logging import logging

Base = declarative_base()


class TimeRecord(Base):
    __tablename__ = "timetable"
    id = Column(Integer, primary_key=True)
    floor = Column(Integer)
    record_time = Column(String)
    username = Column(String)
    username_second = Column(String)
    gender = Column(Integer)

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True)
	username = Column(String)
	telegram_id = Column(Integer)
	is_admin = Column(Boolean)

logging.warning("Connecting to DB...")
engine = create_engine("sqlite:///timetable.db")
Base.metadata.bind = engine
Base.metadata.create_all(engine)

logging.warning("Creating DB session...")
DBSession = sessionmaker(bind=engine)

db = DBSession()
