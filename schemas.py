from pydantic import BaseModel, EmailStr
from models import VehicleType, ReportType
from typing import Optional

# User Models
class UserBase(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True


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
        orm_mode = True


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
        orm_mode = True


# GasSuply Models
class GasSuplyBase(BaseModel):
    gas_stations_id: int

class GasSuplyCreate(GasSuplyBase):
    pass

class GasSuply(GasSuplyBase):
    id: int
    class Config:
        orm_mode = True


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
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None