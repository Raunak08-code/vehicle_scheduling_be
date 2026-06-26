from typing import List, Dict, Any, Optional
import requests

from services.vehicle import VehicleTask


class DepotAPIError(Exception):
    """Depot API call failed."""


EXTERNAL_BASE = "http://4.224.186.213/evaluation-service"


class DepotClient:
    """Fetch depot and vehicle data from the external service."""

    def __init__(self, base_url: str = EXTERNAL_BASE, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url.rstrip("/")
        self.headers = dict(headers or {})

    def fetch_depots(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/depots"
        try:
            resp = requests.get(url, timeout=10, headers=self.headers)
            resp.raise_for_status()
            return resp.json().get("depots", [])
        except Exception as e:
            raise DepotAPIError(f"Failed to fetch depots: {e}")

    def fetch_vehicles(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/vehicles"
        try:
            resp = requests.get(url, timeout=10, headers=self.headers)
            resp.raise_for_status()
            return resp.json().get("vehicles", [])
        except Exception as e:
            raise DepotAPIError(f"Failed to fetch vehicles: {e}")

    def fetch_tasks_for_depot(self, depot_id: int) -> List[VehicleTask]:
        raw = self.fetch_vehicles()
        tasks: List[VehicleTask] = []
        for item in raw:
            task_id = item.get("TaskID") or item.get("taskID") or ""
            duration = item.get("Duration") or item.get("duration") or 0
            impact = item.get("Impact") or item.get("impact") or 0
            tasks.append(
                VehicleTask(
                    id=str(task_id),
                    name=str(item.get("TaskID", "")),
                    duration_hours=int(duration),
                    impact_score=int(impact),
                )
            )
        return tasks


class DepotRequest:
    """Request data bundle for fetching depot tasks."""

    def __init__(self, depot_id: int):
        self.depot_id = depot_id


class DepotResponse:
    """Response container for depot task retrieval."""

    def __init__(self, tasks: List[VehicleTask]):
        self.tasks = tasks
