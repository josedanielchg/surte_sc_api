from sqlalchemy.orm import Session
from seeds_data.gas_stations import gas_stations
import models
import random

def seed_db(db: Session):
    if db.query(models.GasStation).count() == 0:
        # Recorrer el array gas_stations y crear los registros
        for station in gas_stations:
            # Verificar si el barrio ya existe
            neighborhood = db.query(models.Neighborhood).filter(
                models.Neighborhood.name == station["neighborhood_name"],
                models.Neighborhood.city == station["city"],
                models.Neighborhood.state == station["state"]
            ).first()

            # Si el barrio no existe, lo creamos
            if not neighborhood:
                neighborhood = models.Neighborhood(
                    name=station["neighborhood_name"],
                    city=station["city"],
                    state=station["state"]
                )
                db.add(neighborhood)
                db.commit()

            # Crear la estación de gas y asociarla al barrio
            gas_station = models.GasStation(
                name=station["name"],
                image_path=station["image"],
                diesel=station["diesel"],
                latitude=station['latitude'],
                longitude=station['longitude'],
                neighborhood_id=neighborhood.id
            )
            db.add(gas_station)
        db.commit()

    if db.query(models.User).count() == 0:
        # Datos de prueba para User
        users_data = [
            {"username": "John", "email": "john.doe@example.com", "password": "12345678"},
            {"username": "Jane", "email": "jane.smith@example.com", "password": "12345678"},
            {"username": "Admin", "email": "admin@example.com", "password": "12345678"},
            {"username": "Maria", "email": "maria@example.com", "password": "12345678"},
            {"username": "Ariana", "email": "ariana@example.com", "password": "12345678"},
        ]
    
        for user_data in users_data:
            user = models.User(**user_data)
            db.add(user)
        db.commit()

        # Datos de prueba para UserReports
        reports_data = []
        for i in range(1, 20):  
            random_user_id = random.randint(1, 4)  
            random_approx_vehicle = random.randint(3, 14)  
            reports_data.append({"approx_vehicle": random_approx_vehicle, "vehicle_type": "CAR", "type": "QUEUED", "user_id": random_user_id, "gas_stations_id": i})
            reports_data.append({"approx_vehicle": random_approx_vehicle, "vehicle_type": "MOTORCYCLE", "type": "OUT_OF_GAS", "user_id": random_user_id, "gas_stations_id": i})
        
        for report_data in reports_data:
            report = models.UserReports(**report_data)
            db.add(report)
        db.commit()
