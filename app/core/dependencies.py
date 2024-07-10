
from app.core.database import SessionLocal


def get_db():
  ''' Method for configure database '''
  db = SessionLocal()
  try:
      yield db
  finally:
      db.close()
    