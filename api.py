import environment.environment

import os
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Depends, File, UploadFile
from pydantic import BaseModel

from src.api.logger import create_logger

from src.predict import load_yolo_model, yolo_api_prediction


logger = create_logger()

app = FastAPI()

start_time = datetime.now()

logger.info(f'API is ON: {start_time}', exc_info=True)


yolo_model = load_yolo_model(os.path.join('.', 'runs', 'detect', 'train', 'weights', 'best.pt')) 


class APIInput(BaseModel):
    request_id: int = 0
    threshold: float = 0.5


@app.get("/status")
async def get_api_status():
    uptime = (datetime.now() - start_time).total_seconds()
    return {
        "status": "OK",
        "uptime_seconds": uptime,
        "start_time": start_time,
        "current_time": datetime.now()
    }


@app.post("/image_detect")
async def image_detect(input_instance: APIInput = Depends(APIInput), file: UploadFile = File(...)):
    return yolo_api_prediction(input_instance, 'image_detect', logger, yolo_model, file)


if __name__ == "__main__":
    port = os.getenv("PORT")
    uvicorn.run("api:app", port=int(port) if port else 9000, reload=True)