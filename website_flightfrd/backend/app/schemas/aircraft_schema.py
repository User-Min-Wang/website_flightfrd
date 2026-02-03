from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date


class AircraftSchema(BaseModel):
    icao_code: str = Field(..., min_length=6, max_length=6, description="ICAO hex code")
    registration: Optional[str] = Field(None, max_length=10, description="Aircraft registration")
    airline: Optional[str] = Field(None, max_length=100, description="Airline name")
    model: Optional[str] = Field(None, max_length=100, description="Aircraft model")
    type_code: Optional[str] = Field(None, max_length=10, description="IATA type code")
    serial_number: Optional[str] = Field(None, max_length=50, description="Serial number")
    operator: Optional[str] = Field(None, max_length=100, description="Operator/Owner")
    built_date: Optional[date] = Field(None, description="Date of manufacture")
    status: Optional[str] = Field("active", regex=r"^(active|retired|stored)$", description="Status of aircraft")
    first_flight_date: Optional[date] = Field(None, description="First flight date")
    registration_date: Optional[date] = Field(None, description="Registration date")
    registration_expiry: Optional[date] = Field(None, description="Registration expiry date")

    @validator('icao_code')
    def validate_icao_code(cls, v):
        if not v or len(v) != 6:
            raise ValueError('ICAO code must be exactly 6 characters')
        if not all(c in '0123456789ABCDEFabcdef' for c in v):
            raise ValueError('ICAO code must contain only hexadecimal characters')
        return v.upper()

    @validator('registration')
    def validate_registration(cls, v):
        if v and len(v) > 10:
            raise ValueError('Registration must be 10 characters or less')
        return v

    class Config:
        schema_extra = {
            "example": {
                "icao_code": "A2CDEF",
                "registration": "N123AB",
                "airline": "American Airlines",
                "model": "Boeing 737-800",
                "type_code": "738",
                "serial_number": "29012",
                "operator": "American Airlines",
                "built_date": "2018-05-15",
                "status": "active",
                "first_flight_date": "2018-06-20",
                "registration_date": "2018-07-01",
                "registration_expiry": "2028-07-01"
            }
        }