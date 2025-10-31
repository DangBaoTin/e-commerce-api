from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def setup_middleware(app: FastAPI):
    """
    Configures and adds all middleware to the FastAPI application.
    """
    origins = [
        "*",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # List of origins that are allowed
        allow_credentials=True, # Allow cookies
        allow_methods=["*"],    # Allow all methods (GET, POST, etc.)
        allow_headers=["*"],    # Allow all headers
    )
    
    print("Middleware setup complete.")