import os

import dotenv
import motor.motor_asyncio
from fastapi import Body, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.models import LogModel, UpdateLogModel

dotenv.load_dotenv()

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URI"])
db = client.relectric  # Database name


@app.post("/", response_model=LogModel)
async def create_log(log: LogModel = Body(...)):
    """Create a new log in the database."""
    log = jsonable_encoder(log)
    new_log = await db.logs.insert_one(log)
    created_log = await db.logs.find_one({"_id": new_log.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_log)


@app.get("/", response_model=list[LogModel])
async def read_logs():
    """Read all logs from the database."""
    return await db.logs.find().to_list(None)


@app.get("/{log_id}", response_model=LogModel)
async def read_log(log_id: str):
    """Read a log from the database."""
    if (log := await db.logs.find_one({"_id": log_id})) is not None:
        return log
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")


@app.put("/{log_id}", response_model=LogModel)
async def update_log(log_id: str, log: UpdateLogModel = Body(...)):
    """Update a log in the database."""
    log = log.dict(exclude_none=True)

    # Update log if at least 1 value was provided
    if len(log) >= 1:
        update_result = await db.logs.update_one({"_id": log_id}, {"$set": log})
        if update_result.modified_count == 1:
            if (updated_log := await db.logs.find_one({"_id": log_id})) is not None:
                return updated_log

    # Default to existing log if nothing was updated
    if (existing_log := await db.logs.find_one({"_id": log_id})) is not None:
        return existing_log

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")


@app.delete("/{log_id}")
async def delete_log(log_id: str):
    """Delete a log from the database."""
    delete_result = await db.logs.delete_one({"_id": log_id})
    if delete_result.deleted_count == 0:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"deleted": True})
