

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, status
from uuid import UUID
from fastapi.security import OAuth2PasswordBearer

import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from app.accounts.schemas import UserSchema
from app.dependencies import get_db

from .schemas import TokenData
from sqlalchemy.orm import Session
from app.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    try:

        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(email: str, db: Session):
    from app.accounts import services as accounts_crud
    user = accounts_crud.get_user_by_email(db, email)
    if user:
        return user


def authenticate_user(email: str, password: str, db: Session):
    user = get_user(email, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None,
                        expire_time: int = ACCESS_TOKEN_EXPIRE_MINUTES, unit: str = 'minutes'):
    if expires_delta is None:
        expires_delta = calculate_expiration_time(expire_time, unit)

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})

    # Encode the JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def calculate_expiration_time(expire_time: int, unit: str) -> timedelta:
    if unit == 'minutes':
        return timedelta(minutes=expire_time)
    elif unit == 'hours':
        return timedelta(hours=expire_time)
    elif unit == 'days':
        return timedelta(days=expire_time)
    else:
        raise ValueError(
            "Invalid unit for expiration time. Use 'minutes', 'hours', or 'days'.")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="gimme-jwt")

auth_scheme = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)],
    db: Session = Depends(get_db),
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid token or token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(credentials.credentials,
                             SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception

    from app.accounts import services as accounts_crud
    user = accounts_crud.get_user_by_email(db, token_data.email)

    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    request: Request
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    request.state.user = current_user
    return current_user


async def get_current_organisation(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)],
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token or token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(credentials.credentials,
                             SECRET_KEY, algorithms=[ALGORITHM])

        token_data: UUID = payload.get("organisation_id")

        if token_data is None:
            raise credentials_exception

        try:
            token_data: UUID = UUID(token_data)
        except ValueError:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception
    from app.core.dependency_injection import service_locator
    from app.organisation.models import Organisation

    organisation = service_locator.general_service.filter_data(
        db, {"id": token_data}, Organisation, True)

    if organisation is None:
        raise credentials_exception
    return organisation


async def get_current_active_organisation(
    current_organisation: Annotated[UserSchema, Depends(get_current_organisation)],
    request: Request
):

    if not current_organisation.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_organisation
