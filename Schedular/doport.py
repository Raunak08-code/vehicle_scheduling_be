from typing import List

from Schedular.vehicle import VehicleTask


class DepotAPIError(Exception):
    """Raised when depot data cannot be loaded."""
    pass


class DepotClient:
    """Simple depot client to load maintenance tasks for a depot."""

    def __init__(self, depot_id: str):
        self.depot_id = depot_id

    def get_tasks(self) -> List[VehicleTask]:
        """Return a list of tasks for this depot.

        This method currently returns a sample task list. Replace the body
        with a real API call to fetch depot maintenance task details.
        """
        if not self.depot_id:
            raise DepotAPIError("Depot ID is required")

        return [
            VehicleTask(id="A", name="Truck A", duration_hours=3, impact_score=10),
            VehicleTask(id="B", name="Van B", duration_hours=2, impact_score=6),
            VehicleTask(id="C", name="Car C", duration_hours=4, impact_score=12),
            VehicleTask(id="D", name="Bus D", duration_hours=1, impact_score=3),
        ]


class DepotRequest:
    """Request data bundle for fetching depot tasks."""

    def __init__(self, depot_id: str):
        self.depot_id = depot_id


class DepotResponse:
    """Response container for depot task retrieval."""

    def __init__(self, tasks: List[VehicleTask]):
        self.tasks = tasks
