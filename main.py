from fastapi import FastAPI


from authsystem.routs import router as user_router
from authsystem.authentication import router as auth_router

from database import BASE, engine


BASE.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)