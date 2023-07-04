from sqlalchemy.orm import Session

from config import USER_MODEL, USER_CREATE_SCHEMA

def get_user(db: Session, user_id: int):
    return db.query(USER_MODEL).filter(USER_MODEL.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(USER_MODEL).filter(USER_MODEL.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(USER_MODEL).filter(USER_MODEL.username == username).first()

def get_users(db: Session, skip = 0, limit = 100):
    return db.query(USER_MODEL).offset(skip).limit(limit).all()

def update_user(db: Session, user: dict, user_id: int):
    db.query(USER_MODEL).filter(USER_MODEL.id == user_id).update(user)
    db.commit()
    return user

def create_user(db: Session, user: USER_CREATE_SCHEMA):
    db_user = USER_MODEL(
                    email=user.email,
                    username=user.username,
                    password=user.password,)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db.query(USER_MODEL).filter(USER_MODEL.id == user_id).delete()
    db.commit()
    return True 