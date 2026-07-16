import os
from collections.abc import Iterator

from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

DATABASE_URL= os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("environemnt variable missing")

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread":False}
)

Base = declarative_base()

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

def get_db()->Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


