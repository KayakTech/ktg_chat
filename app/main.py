
from fastapi import FastAPI
from app.core.routes import router as core_router
from app.authentication.routes import router as auth_router
from app.accounts.routes import router as accounts_router
from app.organisation.routes import router as projects_router
from app.chat.routes import router as room_router

# from fastapi_amis_admin.admin.site import AdminSite

from app.accounts.models import User
from app.database import engine


from sqladmin import Admin, ModelView


app = FastAPI()

admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]


admin.add_view(UserAdmin)

# create AdminSite instance
# site = AdminSite(settings=Settings(database_url=SQLALCHEMY_DATABASE_URL))

# mount AdminSite instance
# site.mount_app(app)


app.include_router(core_router, tags=["core"])
app.include_router(auth_router, tags=["auhentication"])
app.include_router(accounts_router, prefix="/accounts", tags=["users"])
app.include_router(projects_router, prefix="/organisations",
                   tags=["organisations"])

app.include_router(room_router, prefix="/rooms", tags=["rooms"])
