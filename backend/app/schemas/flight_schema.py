from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class FlightSchema(BaseModel):
    flight_number: Optional[str] = Field(None, max_length=10, description="Flight number (e.g., AA123)")
    callsign: Optional[str] = Field(None, max_length=10, description="Radio callsign")
    aircraft_id: int = Field(..., gt=0, description="ID of associated aircraft")
    departure_airport: Optional[str] = Field(None, max_length=10, description="Departure airport ICAO code")
    arrival_airport: Optional[str] = Field(None, max_length=10, description="Arrival airport ICAO code")
    departure_time: Optional[datetime] = Field(None, description="Scheduled departure time")
    arrival_time: Optional[datetime] = Field(None, description="Scheduled arrival time")
    actual_departure: Optional[datetime] = Field(None, description="Actual departure time")
    actual_arrival: Optional[datetime] = Field(None, description="Actual arrival time")
    status: Optional[str] = Field("scheduled", regex=r"^(scheduled|active|landed|cancelled|delayed)$", 
                                  description="Flight status")
    origin_country: Optional[str] = Field(None, max_length=100, description="Origin country")
    destination_country: Optional[str] = Field(None, max_length=100, description="Destination country")
    altitude: Optional[int] = Field(None, ge=0, description="Current altitude in feet")
    ground_speed: Optional[float] = Field(None, ge=0, description="Ground speed in knots")
    vertical_rate: Optional[float] = Field(None, description="Vertical rate in ft/min")
    heading: Optional[float] = Field(None, ge=0, le=360, description="Heading in degrees")
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Current latitude")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Current longitude")
    on_ground: Optional[bool] = Field(None, description="Whether aircraft is on ground")
    squawk: Optional[str] = Field(None, max_length=4, description="Transponder code")
    baro_altitude: Optional[int] = Field(None, ge=0, description="Barometric altitude")
    true_track: Optional[float] = Field(None, ge=0, le=360, description="True track angle")
    last_position_update: Optional[datetime] = Field(None, description="Last position update timestamp")

    @validator('flight_number')
    def validate_flight_number(cls, v):
        if v and len(v) > 10:
            raise ValueError('Flight number must be 10 characters or less')
        return v

    @validator('squawk')
    def validate_squawk(cls, v):
        if v and not (v.isdigit() and len(v) == 4 and all(c in '01234567' for c in v)):
            raise ValueError('Squawk code must be 4 digits between 0-7')
        return v

    @validator('latitude')
    def validate_latitude(cls, v):
        if v is not None and not (-90 <= v <= 90):
            raise ValueError('Latitude must be between -90 and 90')
        return v

    @validator('longitude')
    def validate_longitude(cls, v):
        if v is not None and not (-180 <= v <= 180):
            raise ValueError('Longitude must be between -180 and 180')
        return v

    class Config:
        schema_extra = {
            "example": {
                "flight_number": "AA123",
                "callsign": "AAL123",
                "aircraft_id": 1,
                "departure_airport": "KJFK",
                "arrival_airport": "KLAX",
                "departure_time": "2023-05-15T08:00:00Z",
                "arrival_time": "2023-05-15T11:30:00Z",
                "status": "active",
                "origin_country": "United States",
                "destination_country": "United States",
                "altitude": 35000,
                "ground_speed": 450.5,
                "heading": 270.0,
                "latitude": 40.7128,
                "longitude": -74.0060,
                "on_ground": False,
                "squawk": "1200"
            }
        }