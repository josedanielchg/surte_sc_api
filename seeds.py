from sqlalchemy.orm import Session
from seeds_data.gas_stations import gas_stations
import models

def seed_db(db: Session):
    if db.query(models.User).count() == 0:
        # Seeding Users
        user1 = models.User(username="john", email="john.doe@example.com", password="securepassword")
        user2 = models.User(username="jane", email="jane.smith@example.com", password="anothersecurepassword")
        
        db.add(user1)
        db.add(user2)
        
        # Seeding other models...
        # neighborhood1 = models.Neighborhood(...)
        # ...
        
        db.commit()
    
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

