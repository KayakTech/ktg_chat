

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ORGANISATION_TOKEN_EXPIRE_DAYS = int(
    os.getenv("ORGANISATION_TOKEN_EXPIRE_DAYS"))


SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
