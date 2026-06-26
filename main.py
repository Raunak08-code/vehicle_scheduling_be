from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from services.schedule import MaintenanceScheduler
from services.vehicle import ScheduleRequest, ScheduleResponse, DepotsResponse, VehiclesResponse
from services.doport import DepotClient, DepotAPIError

app = FastAPI()

@app.get("/")
async def read_root():
    return {"service": "vehicle maintenance scheduler", "status": "ok"}

@app.post("/schedule", response_model=ScheduleResponse)
async def schedule_tasks(request: ScheduleRequest):
    scheduler = MaintenanceScheduler(request.tasks, request.available_hours)
    response = scheduler.compute_best_schedule()
    return response

@app.get("/depots", response_model=DepotsResponse)
async def get_depots():
    client = DepotClient()
    try:
        depots = client.fetch_depots()
        return JSONResponse(content={"depots": depots})
    except DepotAPIError as e:
        raise HTTPException(status_code=502, detail=str(e))

@app.get("/vehicles", response_model=VehiclesResponse)
async def get_vehicles():
    client = DepotClient()
    try:
        vehicles = client.fetch_vehicles()
        # ensure the response is the expected structure
        return JSONResponse(content={"vehicles": vehicles})
    except DepotAPIError as e:
        raise HTTPException(status_code=502, detail=str(e))

@app.get("/depots/{depot_id}/tasks", response_model=ScheduleResponse)
async def get_tasks_for_depot(depot_id: int, available_hours: int = 8):
    client = DepotClient()
    try:
        tasks = client.fetch_tasks_for_depot(depot_id)
        scheduler = MaintenanceScheduler(tasks, available_hours)
        return scheduler.compute_best_schedule()
    except DepotAPIError as e:
        raise HTTPException(status_code=502, detail=str(e))

