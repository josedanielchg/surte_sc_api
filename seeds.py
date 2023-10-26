from sqlalchemy.orm import Session
import models

def seed_db(db: Session):
    if db.query(models.User).count() == 0:
        # Seeding Users
        user1 = models.User(email="john.doe@example.com", password="securepassword")
        user2 = models.User(email="jane.smith@example.com", password="anothersecurepassword")
        
        db.add(user1)
        db.add(user2)
        
        # Seeding other models...
        # neighborhood1 = models.Neighborhood(...)
        # ...
        
        db.commit()
    
    if db.query(models.GasStation).count() == 0:
        # Seeding Users
        user1 = models.User(email="john.doe@example.com", password="securepassword")
        
        db.add(user1)
        db.commit()
