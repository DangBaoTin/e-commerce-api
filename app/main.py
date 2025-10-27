# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import init_db
from app.api.endpoints import users  # <--- Import the user router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("FastAPI app starting up...")
    await init_db()
    yield
    print("FastAPI app shutting down...")

app = FastAPI(
    title="E-Commerce API",
    description="A simple API for an e-commerce platform.",
    version="0.1.0",
    lifespan=lifespan
)

# --- Include Routers ---
# This line "plugs in" all the routes from users.py
# at the prefix /api/v1/users
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-Commerce API!"}