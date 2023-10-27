from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, joinedload
from main import models, schemas, utils, oauth2
from dependencies import get_db
from typing import Optional, List

router = APIRouter()

TIME_BY_VEHICLE = 3

@router.get('/gas_stations/')
def get_gas_stations(
    db: Session = Depends(get_db),
    user_id: str = Depends(oauth2.get_current_user),
    neighborhood_name: Optional[str] = None  # Añadimos un nuevo parámetro para el filtro
):
    # Si neighborhood_name no es None, filtramos por ese valor. De lo contrario, traemos todos.
    query = db.query(models.GasStation).options(
        joinedload(models.GasStation.neighborhood),  # Carga relacionada con Neighborhood
        joinedload(models.GasStation.gas_supplies)   # Carga relacionada con GasSuply
    )
    
    if neighborhood_name:
        query = query.join(models.Neighborhood).filter(models.Neighborhood.name.ilike(f"%{neighborhood_name}%"))

    gas_stations = query.all()

    # Para cada estación de gasolina, obtener el último UserReport relacionado
    for station in gas_stations:
        station.latest_report = (
            db.query(models.UserReports)
            .filter(models.UserReports.gas_stations_id == station.id)
            .order_by(models.UserReports.created_at.desc())
            .first()
        )

    # Setear el tiempo estimado
    for station in gas_stations:
        if station.latest_report:
            approx_vehicle = station.latest_report.approx_vehicle
            station.estimated_time = approx_vehicle * TIME_BY_VEHICLE

    return gas_stations


@router.get('/gas_stations/{station_id}')
def get_gas_station_by_id(station_id: int, db: Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user)):
    gas_station = (
        db.query(models.GasStation)
        .options(joinedload(models.GasStation.neighborhood))  # Carga relacionada con Neighborhood
        .options(joinedload(models.GasStation.gas_supplies))  # Carga relacionada con GasSuply
        .filter(models.GasStation.id == station_id)
        .first()
    )

    if not gas_station:
        raise HTTPException(status_code=404, detail="Gas station not found")

    # Obtener el último UserReport relacionado con la estación de gasolina
    gas_station.latest_report = (
        db.query(models.UserReports)
        .filter(models.UserReports.gas_stations_id == gas_station.id)
        .order_by(models.UserReports.created_at.desc())
        .first()
    )

    if gas_station.latest_report:
        approx_vehicle = gas_station.latest_report.approx_vehicle
        gas_station.estimated_time = approx_vehicle * TIME_BY_VEHICLE
    
    return gas_station
