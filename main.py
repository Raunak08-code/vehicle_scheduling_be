from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List

from Schedular.schedule import select_vehicle_tasks
from Schedular.vehicle import VehicleTask, ScheduleRequest, ScheduleResponse

app = FastAPI()

@app.get("/")
async def read_root():
    return {"service": "vehicle maintenance scheduler", "status": "ok"}

@app.post("/schedule", response_model=ScheduleResponse)
async def schedule_tasks(request: ScheduleRequest):
    selected_tasks, total_hours, total_score = select_vehicle_tasks(request.tasks, request.available_hours)
    response = {
        "selected_tasks": selected_tasks,
        "total_duration_hours": total_hours,
        "total_impact_score": total_score,
    }
    return JSONResponse(content=response)

