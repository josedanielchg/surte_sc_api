from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, joinedload
from main import models, schemas, utils, oauth2
from dependencies import get_db
from typing import Optional, List

router = APIRouter()

@router.get('/gas_stations/')
def get_gas_stations(db: Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user)):
    gas_stations = (
        db.query(models.GasStation)
        .options(joinedload(models.GasStation.neighborhood))  # Carga relacionada con Neighborhood
        .options(joinedload(models.GasStation.gas_supplies))  # Carga relacionada con GasSuply
        .all()
    )

    # Para cada estación de gasolina, obtener el último UserReport relacionado
    for station in gas_stations:
        station.latest_report = (
            db.query(models.UserReports)
            .filter(models.UserReports.gas_stations_id == station.id)
            .order_by(models.UserReports.created_at.desc())
            .first()
        )

    return gas_stations