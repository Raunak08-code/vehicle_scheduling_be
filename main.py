from fastapi import FastAPI

from Schedular.schedule import MaintenanceScheduler
from Schedular.vehicle import ScheduleRequest, ScheduleResponse

app = FastAPI()

@app.get("/")
async def read_root():
    return {"service": "vehicle maintenance scheduler", "status": "ok"}

@app.post("/schedule", response_model=ScheduleResponse)
async def schedule_tasks(request: ScheduleRequest):
    scheduler = MaintenanceScheduler(request.tasks, request.available_hours)
    response = scheduler.compute_best_schedule()
    return response

