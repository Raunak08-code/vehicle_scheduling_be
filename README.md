# Vehicle Maintenance Scheduler Microservice

A simple FastAPI microservice that selects maintenance tasks to maximize operational impact without exceeding available mechanic hours.

## Project structure

- `main.py` - FastAPI application with `/schedule` endpoint.
- `Schedular/vehicle.py` - request and task models.
- `Schedular/schedule.py` - scheduling logic.
- `requirements.txt` - Python dependencies.

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

## API

### POST /schedule

Request body:

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

Response:

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

## Notes

This service uses a 0/1 knapsack algorithm to choose the best combination of tasks.
