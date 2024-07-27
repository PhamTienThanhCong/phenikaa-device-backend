from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.core.setting import get_setting


class DeviceCategoryService:
  def __init__(self):
    self.base = get_setting()
    pass