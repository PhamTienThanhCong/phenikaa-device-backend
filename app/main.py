from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount the public directory
app.mount("/public", StaticFiles(directory="public"), name="public")

@app.get("/health")
async def root():
    return "oke"
