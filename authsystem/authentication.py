from datetime import timedelta
from sqlalchemy.orm import Session

from jose import jwt, JWTError

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import  APIRouter, HTTPException, Depends, status

from database import SESSION_LOCAL
from .schemas import Token, TokenData
from config import (
    USER_DEFAULT_SCHEMA,ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(
    tags=["Authentication"],
)

def get_db():
    db = SESSION_LOCAL()
    try:
        yield db
    finally:
        db.close()

from .context import (
    oauth2_scheme,
    SECRET_KEY,
    ALGORITHM,
    get_user,
    authenticate_user,
    create_access_token,
)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: USER_DEFAULT_SCHEMA = Depends(get_current_user)):
    return current_user

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=USER_DEFAULT_SCHEMA)
async def read_users_me(current_user: USER_DEFAULT_SCHEMA = Depends(get_current_active_user)):
    return current_user