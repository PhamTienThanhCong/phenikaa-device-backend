import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers.api import router as router_api
from fastapi.responses import HTMLResponse
from app.core.database import Base, engine

app = FastAPI()

# Mount the public directory
app.mount("/public", StaticFiles(directory="public"), name="public")

origins = ["http://localhost:3000", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(router_api, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open(os.path.join("public", "index.html")) as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/health")
async def root():
    return "oke"
