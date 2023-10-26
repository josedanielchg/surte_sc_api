from sqlalchemy import Boolean, Column, Integer, Float, String, TIMESTAMP, BOOLEAN, Enum as SQLEnum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum
import datetime

# ===
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    email = Column(String(50), unique=True)
    password = Column(String(150))
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


# ===
class Neighborhood(Base):
    __tablename__ = 'neighborhoods'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45))
    city = Column(String(45))
    state = Column(String(45))
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


# ===
class GasStation(Base):
    __tablename__ = 'gas_stations'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), unique=True)
    image_path = Column(String(255))
    diesel = Column(BOOLEAN)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    neighborhood_id = Column(Integer, ForeignKey('neighborhoods.id'))

    neighborhood = relationship("Neighborhood", back_populates="gas_stations")

Neighborhood.gas_stations = relationship("GasStation", order_by=GasStation.id, back_populates="neighborhood")

# ===
class GasSuply(Base):
    __tablename__ = 'gas_supply'
    
    id = Column(Integer, primary_key=True, index=True)
    gas_stations_id = Column(Integer, ForeignKey('gas_stations.id'))
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    gas_station = relationship("GasStation", back_populates="gas_supplies")

GasStation.gas_supplies = relationship("GasSuply", order_by=GasSuply.id, back_populates="gas_station")
    
    
# ===
class VehicleType(Enum):
    CAR = "CARRO"
    MOTORCYCLE = "MOTO"
    
class ReportType(str, Enum):
    queued = "QUEUED"
    out_of_gas = "OUT_OF_GAS"

class UserReports(Base):
    __tablename__ = 'user_reports'
    
    id = Column(Integer, primary_key=True, index=True)
    approx_vehicle = Column(Integer)
    vehicle_type = Column(SQLEnum(VehicleType))
    type = Column(SQLEnum(ReportType))
    user_id = Column(Integer, ForeignKey('users.id'))
    gas_stations_id = Column(Integer, ForeignKey('gas_stations.id'))
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)