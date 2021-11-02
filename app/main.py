import os

import dotenv
import motor.motor_asyncio
from fastapi import Body, FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.models import LogModel

dotenv.load_dotenv()

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URI"])
db = client["relectric"]  # Database name


@app.post("/")
async def create_log(log: LogModel = Body(...)):
    """Create a new log in the database."""
    log = jsonable_encoder(log)
    new_log = await db["logs"].insert_one(log)
    created_log = await db["logs"].find_one({"_id": new_log.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_log)
