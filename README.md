# Vehicle Maintenance Scheduler Microservice

This repository contains a FastAPI microservice that solves a daily vehicle maintenance scheduling problem.

The service receives a list of maintenance tasks, each with:
- `duration_hours` — estimated mechanic hours required
- `impact_score` — operational importance of completing the task

The solver picks the best subset of tasks such that:
- the total mechanic hours does not exceed the available budget
- the total impact score is maximized

## Project structure

- `main.py` - FastAPI application with `/schedule` endpoint.
- `services/vehicle.py` - Pydantic models for tasks and request/response payloads.
- `services/schedule.py` - knapsack-based scheduling algorithm.
- `services/doport.py` - external depot and vehicle API client.
- `requirements.txt` - Python dependencies.
- `sample_request.json` - example request payload.
- `test_schedule.py` - simple unit test.

## Install

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the automatically generated API documentation.

## API

### POST /schedule

Send a JSON body with the available mechanic hours and the maintenance tasks.

Example request body:

```json
{
  "available_hours": 5,
  "tasks": [
    {"id":"A","name":"Truck A","duration_hours":3,"impact_score":10},
    {"id":"B","name":"Van B","duration_hours":2,"impact_score":6},
    {"id":"C","name":"Car C","duration_hours":4,"impact_score":12}
  ]
}
```

Example response:

```json
{
  "selected_tasks": [
    {"id":"A","name":"Truck A","duration_hours":3,"impact_score":10},
    {"id":"B","name":"Van B","duration_hours":2,"impact_score":6}
  ],
  "total_duration_hours": 5,
  "total_impact_score": 16
}
```

### GET /depots

Returns the list of depots fetched from the external evaluation service.

Response schema: `{"depots": [ {"ID": 1, "MechanicHours": 60}, ... ]}`

### GET /vehicles

Returns the list of vehicles/tasks from the external evaluation service.

Response schema: `{"vehicles": [ {"TaskID":"...","Duration":1,"Impact":5}, ... ]}`

### GET /depots/{depot_id}/tasks?available_hours=8

Fetches vehicles, converts them to internal `VehicleTask` models, and returns a computed schedule constrained by `available_hours` (default 8).

## Example curl

```bash
curl -X POST http://127.0.0.1:8000/schedule \
  -H "Content-Type: application/json" \
  -d @sample_request.json
```

Fetch external depots (may require authentication):

```bash
curl http://127.0.0.1:8000/depots
curl http://127.0.0.1:8000/vehicles
```

## Testing

```bash
pytest test_schedule.py
```

## Notes

- The scheduler uses an efficient dynamic programming algorithm to handle large task lists.
- The `/depots` and `/vehicles` endpoints proxy the external APIs at `http://4.224.186.213/evaluation-service` and may require authentication in the real evaluation environment. If the external API is protected, update `Schedular/doport.py` to attach the correct auth headers (bearer token or similar).
