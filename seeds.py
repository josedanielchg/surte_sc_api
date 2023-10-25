from sqlalchemy.orm import Session
import models

def seed_db(db: Session):
    # Seeding Users
    user1 = models.User(email="john.doe@example.com", password="securepassword")
    user2 = models.User(email="jane.smith@example.com", password="anothersecurepassword")
    
    db.add(user1)
    db.add(user2)

    # Seeding other models...
    # neighborhood1 = models.Neighborhood(...)
    # ...
    
    db.commit()
