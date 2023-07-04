from authsystem.models import UserBaseModel
from authsystem.schemas import User as UserSchema, UserCreateSchema

## Secret setrings

SECRET_KEY = "thequickbrownfoxjumpedoverthelazydog"

## Token

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

## AUTH Settings

USER_MODEL = UserBaseModel
USER_DEFAULT_SCHEMA = UserSchema
USER_CREATE_SCHEMA = UserCreateSchema