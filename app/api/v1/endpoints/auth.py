# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import Token
from app.services.auth_service import auth_service

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Logs in a user and returns an access token.
    """
    # Call the service layer
    access_token = await auth_service.login(
        username=form_data.username,
        password=form_data.password
    )
    
    # Handle the service's response
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"access_token": access_token, "token_type": "bearer"}