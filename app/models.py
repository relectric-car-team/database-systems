from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


# MongoDB uses BSON but Python uses JSON so we must convert ObjectIds to strings
class PyObjectId(ObjectId):
    # Required methods for proper validation and updating
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError(f"{v} is not a valid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="str")


class LogModel(BaseModel):
    # Alias id to _id so we can refer to it by id and have Mongo handle it correctly
    id: PyObjectId = Field(
        default_factory=PyObjectId, alias="_id"
    )  # Default to PyObjectId
    severity: str = Field(...)
    message: str = Field(...)
    timestamp: datetime = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "severity": "INFO",
                "message": "This is a test message",
                "timestamp": datetime.now(),
            }
        }


class UpdateLogModel(BaseModel):
    severity: Optional[str]
    message: Optional[str]
    timestamp: Optional[datetime]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "severity": "INFO",
                "message": "This is a test message",
                "timestamp": datetime.now(),
            }
        }


class GPSLogModel(BaseModel):
    id: PyObjectId = Field(
        default_factory=PyObjectId, alias="_id"
    )  # Default to PyObjectId
    sentence: str = Field(...)
    timestamp: datetime = Field(...)
    latitude: float = Field(...)
    longitude: float = Field(...)
    altitude: float = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "sentence": "GPGGA",
                "timestamp": 1642556325,
                "latitude": 40.730610,
                "longitude": -73.935242,
                "altitude": 1244.1,
            }
        }
