from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from models import VehicleType, ReportType
from schemas import UserBase, UserCreate, User, NeighborhoodBase, NeighborhoodCreate, Neighborhood, GasStationBase, GasStationCreate, GasStation, GasSuplyBase, GasSuplyCreate, GasSuply, UserReportsBase, UserReportsCreate, UserReports
import models, seeds
from routers import user

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

app.include_router(user.router)
app.include_router(auth.router)