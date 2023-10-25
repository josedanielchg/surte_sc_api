from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models import VehicleType, ReportType
from schemas import UserBase, UserCreate, User, NeighborhoodBase, NeighborhoodCreate, Neighborhood, GasStationBase, GasStationCreate, GasStation, GasSuplyBase, GasSuplyCreate, GasSuply, UserReportsBase, UserReportsCreate, UserReports
import models
import seeds

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

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


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()