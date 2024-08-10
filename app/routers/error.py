from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile

router = APIRouter(prefix="/test-error", tags=["error"])


@router.get("")
def get_error():
    return 0/1


@router.post("")
def get_error():
    return 0/1


@router.put("")
def get_error():
    return 0/1


@router.delete("")
def get_error():
    return 0/1
