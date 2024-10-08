from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent


DB_PATH = os.path.join(BASE_DIR, 'sql_app.db')
print(DB_PATH)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"


# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
