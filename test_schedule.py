from Schedular.schedule import MaintenanceScheduler
from Schedular.vehicle import VehicleTask


def test_select_vehicle_tasks():
    tasks = [
        VehicleTask(id="A", name="Truck A", duration_hours=3, impact_score=10),
        VehicleTask(id="B", name="Van B", duration_hours=2, impact_score=6),
        VehicleTask(id="C", name="Car C", duration_hours=4, impact_score=12),
        VehicleTask(id="D", name="Bus D", duration_hours=1, impact_score=3),
    ]

    scheduler = MaintenanceScheduler(tasks, 5)
    response = scheduler.compute_best_schedule()

    assert response.total_duration_hours == 5
    assert response.total_impact_score == 16
    assert [task.id for task in response.selected_tasks] == ["A", "B"]
