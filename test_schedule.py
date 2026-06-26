from Schedular.schedule import select_vehicle_tasks
from Schedular.vehicle import VehicleTask


def test_select_vehicle_tasks():
    tasks = [
        VehicleTask(id="A", name="Truck A", duration_hours=3, impact_score=10),
        VehicleTask(id="B", name="Van B", duration_hours=2, impact_score=6),
        VehicleTask(id="C", name="Car C", duration_hours=4, impact_score=12),
        VehicleTask(id="D", name="Bus D", duration_hours=1, impact_score=3),
    ]

    selected, total_hours, total_score = select_vehicle_tasks(tasks, 5)

    assert total_hours == 5
    assert total_score == 16
    assert [task.id for task in selected] == ["A", "B"]
