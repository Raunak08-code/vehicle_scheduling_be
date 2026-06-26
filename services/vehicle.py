from pydantic import BaseModel, Field
from typing import List

class VehicleTask(BaseModel):
    id: str = Field(..., description="Unique identifier for the maintenance task")
    name: str = Field(..., description="Vehicle or task name")
    duration_hours: int = Field(..., ge=0, description="Estimated mechanic hours for the task")
    impact_score: int = Field(..., ge=0, description="Operational impact score for the task")

class Depot(BaseModel):
    ID: int = Field(..., description="Depot numeric ID")
    MechanicHours: int = Field(..., description="Available mechanic-hours at the depot")

class ScheduleRequest(BaseModel):
    available_hours: int = Field(..., ge=0, description="Daily mechanic-hour budget")
    tasks: List[VehicleTask] = Field(..., description="List of candidate maintenance tasks")

class ScheduleResponse(BaseModel):
    selected_tasks: List[VehicleTask]
    total_duration_hours: int
    total_impact_score: int

class VehicleFromAPI(BaseModel):
    TaskID: str
    Duration: int
    Impact: int

class DepotsResponse(BaseModel):
    depots: List[Depot]

class VehiclesResponse(BaseModel):
    vehicles: List[VehicleFromAPI]
