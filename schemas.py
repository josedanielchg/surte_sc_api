from pydantic import BaseModel, EmailStr
from models import VehicleType, ReportType
from typing import Optional
from datetime import datetime

# User Models
class UserBase(BaseModel):
    email: str
    username: str
    password: str

class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes  = True
        
class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime

    class Config:
        from_attributes  = True

# Neighborhood Models
class NeighborhoodBase(BaseModel):
    name: str
    city: str
    state: str

class NeighborhoodCreate(NeighborhoodBase):
    pass

class Neighborhood(NeighborhoodBase):
    id: int
    class Config:
        from_attributes  = True


# GasStation Models
class GasStationBase(BaseModel):
    name: str
    image_path: str
    diesel: bool
    neighborhood_id: int

class GasStationCreate(GasStationBase):
    pass

class GasStation(GasStationBase):
    id: int
    class Config:
        from_attributes  = True


# GasSuply Models
class GasSuplyBase(BaseModel):
    gas_stations_id: int

class GasSuplyCreate(GasSuplyBase):
    pass

class GasSuply(GasSuplyBase):
    id: int
    class Config:
        from_attributes  = True


# UserReports Models
class UserReportsBase(BaseModel):
    approx_vehicle: int
    vehicle_type: VehicleType
    type: ReportType
    user_id: int
    gas_stations_id: int

class UserReportsCreate(UserReportsBase):
    pass

class UserReports(UserReportsBase):
    id: int
    class Config:
        from_attributes  = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None