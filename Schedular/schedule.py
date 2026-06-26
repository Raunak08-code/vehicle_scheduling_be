from typing import List, Tuple

from Schedular.vehicle import VehicleTask


def select_vehicle_tasks(tasks: List[VehicleTask], available_hours: int) -> Tuple[List[VehicleTask], int, int]:
    """Select the subset of tasks that maximizes total impact score within the available mechanic hours."""
    if available_hours <= 0 or not tasks:
        return [], 0, 0

    budget = available_hours
    n = len(tasks)
    # dp[w] = maximum score achievable with w hours
    dp = [0] * (budget + 1)
    choice = [-1] * (budget + 1)
    prev = [-1] * (budget + 1)

    for idx, task in enumerate(tasks):
        weight = task.duration_hours
        value = task.impact_score
        if weight > budget:
            continue
        for w in range(budget, weight - 1, -1):
            candidate_score = dp[w - weight] + value
            if candidate_score > dp[w]:
                dp[w] = candidate_score
                choice[w] = idx
                prev[w] = w - weight

    best_hours = max(range(budget + 1), key=lambda w: dp[w])
    total_score = dp[best_hours]

    selected_indices = []
    current = best_hours
    while current > 0 and choice[current] != -1:
        selected_indices.append(choice[current])
        current = prev[current]

    selected_indices.reverse()
    selected_tasks = [tasks[i] for i in selected_indices]
    total_hours = sum(task.duration_hours for task in selected_tasks)

    return selected_tasks, total_hours, total_score
