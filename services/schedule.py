from typing import List

from services.vehicle import VehicleTask, ScheduleResponse


class MaintenanceScheduler:
    def __init__(self, tasks: List[VehicleTask], available_hours: int):
        self.tasks = tasks
        self.available_hours = max(0, available_hours)
        self.selected_tasks: List[VehicleTask] = []
        self.total_duration_hours = 0
        self.total_impact_score = 0

    def compute_best_schedule(self) -> ScheduleResponse:
        self._compute_knapsack()
        return ScheduleResponse(
            selected_tasks=self.selected_tasks,
            total_duration_hours=self.total_duration_hours,
            total_impact_score=self.total_impact_score,
        )

    def _compute_knapsack(self) -> None:
        if self.available_hours <= 0 or not self.tasks:
            self.selected_tasks = []
            self.total_duration_hours = 0
            self.total_impact_score = 0
            return

        budget = self.available_hours
        dp = [0] * (budget + 1)
        choice = [-1] * (budget + 1)
        prev = [-1] * (budget + 1)

        for idx, task in enumerate(self.tasks):
            weight = task.duration_hours
            value = task.impact_score
            if weight > budget:
                continue
            for w in range(budget, weight - 1, -1):
                score = dp[w - weight] + value
                if score > dp[w]:
                    dp[w] = score
                    choice[w] = idx
                    prev[w] = w - weight

        best_hours = max(range(budget + 1), key=lambda w: dp[w])
        self.total_impact_score = dp[best_hours]

        selected_indices: List[int] = []
        current = best_hours
        while current > 0 and choice[current] != -1:
            selected_indices.append(choice[current])
            current = prev[current]

        selected_indices.reverse()
        self.selected_tasks = [self.tasks[i] for i in selected_indices]
        self.total_duration_hours = sum(task.duration_hours for task in self.selected_tasks)
