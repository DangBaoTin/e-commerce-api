from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import init_db

from app.api.v1.endpoints import users
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import products
from app.api.v1.endpoints import cart

from app.middleware import setup_middleware

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

setup_middleware(app)

# --- Routers ---
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(cart.router, prefix="/api/v1/cart", tags=["Shopping Cart"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-Commerce API!"}