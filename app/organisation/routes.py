from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.accounts.schemas import UserSchema
from app.authentication.utils import get_current_active_user
from fastapi_utils.cbv import cbv
from app.dependencies import get_db
from app.organisation.schemas import OrganisationSchema, OrganisationResponseSchema
from app.organisation.models import Organisation
from pydantic import UUID4
from app.core.dependency_injection import service_locator
from datetime import timedelta
from app.settings import ORGANISATION_TOKEN_EXPIRE_DAYS
from fastapi import HTTPException, status

from app.authentication.utils import create_access_token


router = APIRouter(

)


@cbv(router)
class ProjectView:
    current_user: UserSchema = Depends(get_current_active_user)
    db: Session = Depends(get_db)

    @router.get("/", response_model=list[OrganisationResponseSchema])
    @router.post("/", response_model=OrganisationSchema)
    async def projects(self, request: Request, data: OrganisationSchema = None):

        if request.method == "GET":
            filter = {
                "user_id": self.current_user.id
            }

            return service_locator.general_service.filter_data(self.db, filter, Organisation)

        data.__dict__['user_id'] = self.current_user.id

        data = Organisation(**data.__dict__)
        exists = self.db.query(Organisation).filter(
            Organisation.email == data.email
        ).one_or_none()

        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "email_exists": "This email already exists for an organisation"}
            )

        response = service_locator.general_service.create_data(self.db, data)
        return response

    @router.get("/{id}", response_model=OrganisationResponseSchema)
    async def get_project(self, id: UUID4):

        project = service_locator.general_service.get_data_by_id(
            self.db, id, Organisation)
        return project

    @router.delete("/{id}")
    async def delete_project(self, id: UUID4):
        project = service_locator.general_service.delete_data(
            self.db, id, Organisation)
        return project

    @router.put("/{id}", response_model=OrganisationSchema)
    @router.patch("/{id}", response_model=OrganisationSchema)
    async def update_project(self, id: UUID4, data: OrganisationSchema):
        data = data.dict(exclude_unset=True)

        updated_project = service_locator.general_service.update_data(
            self.db, key=id, data=data, model=Organisation)

        return updated_project

    @router.post("/generate-token/{organisation_id}", response_model=OrganisationResponseSchema)
    async def generate_organisation(self,  organisation_id: UUID4):

        data = {"organisation_id": str(organisation_id)}
        data = {
            "token": create_access_token(data=data, expires_delta=timedelta(days=ORGANISATION_TOKEN_EXPIRE_DAYS))
        }

        updated_orginisation = service_locator.general_service.update_data(
            self.db, key=organisation_id, data=data, model=Organisation)

        return updated_orginisation
