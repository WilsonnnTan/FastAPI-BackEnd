from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.auth import user
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")