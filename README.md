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
- `Schedular/vehicle.py` - Pydantic models for tasks and request/response payloads.
- `Schedular/schedule.py` - knapsack-based scheduling algorithm.
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

## Example curl

```bash
curl -X POST http://127.0.0.1:8000/schedule \
  -H "Content-Type: application/json" \
  -d @sample_request.json
```

## Testing

```bash
pytest test_schedule.py
```

## Notes

- The scheduler uses an efficient dynamic programming algorithm to handle large task lists.
- External depot/task APIs are not included inside this repository; tasks are provided to the service via the request body.
