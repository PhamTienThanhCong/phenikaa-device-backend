from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile

router = APIRouter(prefix="/test-error", tags=["error"])


@router.get("")
def get_error():
    raise HTTPException(status_code=500, detail="Error")


@router.post("")
def get_error():
    raise HTTPException(status_code=500, detail="Error")


@router.put("")
def get_error():
    raise HTTPException(status_code=500, detail="Error")


@router.delete("")
def get_error():
    raise HTTPException(status_code=500, detail="Error")
