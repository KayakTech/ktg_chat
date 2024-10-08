
from fastapi import APIRouter, Depends, Request

from .schemas import UserResponseSchema, UserSchema
from app.authentication.utils import get_current_active_user

router = APIRouter(
    dependencies=[Depends(get_current_active_user)]
)


@router.get("/me/", response_model=UserResponseSchema)
async def get_account(request: Request):
    current_user: UserSchema = request.state.user
    return current_user
