from fastapi import (
    Depends, 
    HTTPException, 
    status, 
    APIRouter, 
)
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from config import USER_DEFAULT_SCHEMA, USER_CREATE_SCHEMA
from database import SESSION_LOCAL
from config import USER_DEFAULT_SCHEMA


from .context import (
    get_password_hash,
)

from .crud import (
    get_user, 
    get_user_by_email, 
    get_users, 
    create_user, 
    delete_user,
    update_user,
)

ORDERING_BY = []

def get_db():
    db = SESSION_LOCAL()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@router.get("/", response_model=list[USER_DEFAULT_SCHEMA], response_model_exclude=["password",])
async def get_all_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)) -> list[USER_DEFAULT_SCHEMA]:
    return get_users(db=db, skip=skip, limit=limit)

@router.get("/{id}", response_model=USER_DEFAULT_SCHEMA, response_model_exclude=["password",])
async def get_user_by_id_or_email(
    id: str, 
    by: str = "id", 
    db: Session = Depends(get_db)) -> USER_DEFAULT_SCHEMA | HTTPException:
    if by == "id" and id.isnumeric():
        user = get_user(db=db, user_id=int(id))
    elif by == "email":
        user = get_user_by_email(db=db, email=id)
    
    if not user:
        return HTTPException(status.HTTP_404_NOT_FOUND, "User with this params not found")
    
    return user

@router.post("/create", response_model=USER_DEFAULT_SCHEMA)
async def create_new_user(
    user: USER_CREATE_SCHEMA, 
    db: Session = Depends(get_db)) -> USER_DEFAULT_SCHEMA:
    user.password = get_password_hash(user.password)
    return create_user(db=db, user=user)

@router.put("/update/{id}", response_model=USER_CREATE_SCHEMA)
async def update_exists_user(id: int, user: USER_CREATE_SCHEMA, db: Session = Depends(get_db)):
    encoded_user = jsonable_encoder(user)
    update_user(db=db, user=encoded_user, user_id=id)
    return encoded_user

@router.delete("/delete/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_item(
    id: int, 
    db: Session = Depends(get_db)) -> dict:
    delete_user(db=db, user_id=id)
    return {"detail": "User successfuly deleted"}