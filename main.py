from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models, seeds, schemas, utils, oauth2
from routers import user, auth, user_reports 
from  dependencies import get_db

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seed the database
with SessionLocal() as db:
    seeds.seed_db(db)
        
db_dependency = Annotated[Session, Depends(get_db)]

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(user_reports.router)