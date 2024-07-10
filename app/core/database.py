from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USER_DB = "root"
PASSWORD_DB = ""
NAME_DB = "fastapi_db"
PORT_DB = "3306"


SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{USER_DB}:{PASSWORD_DB}@localhost:{PORT_DB}/{NAME_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()