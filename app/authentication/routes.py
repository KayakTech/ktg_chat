

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.authentication import schemas
from app.authentication.utils import authenticate_user, create_access_token
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.accounts import services as accounts_services
from app.accounts.schemas import UserResponseSchema


router = APIRouter()


@router.post("/register/", response_model=UserResponseSchema)
async def register(registation_form: schemas.UserRegistrationForm, db: Session = Depends(get_db)):
    try:

        user = accounts_services.create_user(db, registation_form)

        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/gimme-jwt/", response_model=schemas.Token)
async def gimme_jwt(
    form_data: schemas.LoginForm,
    db: Session = Depends(get_db)
) -> schemas.Token:

    user = authenticate_user(form_data.email, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return schemas.Token(access_token=access_token, token_type="bearer")
