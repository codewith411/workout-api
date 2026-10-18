
# Workout API

## Description

Workout API is a Flask REST API for managing workouts, exercises, and the exercises performed during each workout. It uses SQLAlchemy for database operations, Flask-Migrate for database migrations, and Marshmallow for serialization and validation.

## Features

- Create, view, and delete workouts.
- Create, view, and delete exercises.
- Associate exercises with workouts.
- Record repetitions, sets, and duration for each workout exercise.
- Validate request data before saving it.
- Serialize workouts with their associated exercises.
- Manage database schema changes through Flask-Migrate.
- Reset and populate sample data using a seed script.

## Technologies

- Python 3.8+
- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 3.1.0
- Marshmallow 3.20.1
- SQLite

## Project Structure

```text
workout-api/
├── .gitignore
├── Pipfile
├── README.md
└── server/
    ├── app.py
    ├── models.py
    ├── schemas.py
    ├── seed.py
    └── migrations/
```

## Installation

Clone or download the project and enter its root directory.

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install \
  Flask==2.2.2 \
  Flask-Migrate==3.1.0 \
  Flask-SQLAlchemy==3.0.3 \
  Werkzeug==2.2.2 \
  importlib-metadata==6.0.0 \
  importlib-resources==5.10.0 \
  ipdb==0.13.9 \
  marshmallow==3.20.1
```

## Database Setup

Enter the server directory and configure Flask:

```bash
cd server
export FLASK_APP=app.py
```

Apply the existing database migrations:

```bash
flask db upgrade
```

This creates the database tables from the migration history.

## Seed the Database

From the `server` directory, run:

```bash
python seed.py
```

The seed script clears existing workout, exercise, and association records before inserting three sample exercises, two workouts, and three workout-exercise records.

Running it again resets and repopulates the sample data.

**Warning:** The seed script deletes the existing records in these tables.

## Run the Application

From the `server` directory, run:

```bash
python app.py
```

The API runs at:

`http://127.0.0.1:5555`

Test the home endpoint:

```bash
curl http://127.0.0.1:5555/
```

Expected response:

```json
{
  "message": "Workout API is running!"
}
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| GET | `/exercises` | Retrieve all exercises |
| GET | `/exercises/<exercise_id>` | Retrieve one exercise |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<exercise_id>` | Delete an exercise |
| GET | `/workouts` | Retrieve all workouts |
| GET | `/workouts/<workout_id>` | Retrieve one workout with associated exercise details |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<workout_id>` | Delete a workout |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

### Create an Exercise

Send a POST request to `/exercises`:

```json
{
  "name": "Push-ups",
  "category": "Strength",
  "equipment_needed": false
}
```

Example:

```bash
curl -X POST http://127.0.0.1:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{"name":"Push-ups","category":"Strength","equipment_needed":false}'
```

### Create a Workout

Send a POST request to `/workouts`:

```json
{
  "date": "2026-10-18",
  "duration_minutes": 30,
  "notes": "Morning strength training"
}
```

The date must use the `YYYY-MM-DD` format, and the duration must be a positive integer.

### Add an Exercise to a Workout

Send a POST request to:

`/workouts/1/exercises/1/workout_exercises`

Request body:

```json
{
  "reps": 12,
  "sets": 3,
  "duration_seconds": 60
}
```

The workout and exercise IDs must refer to existing records. The response includes the new association and the related exercise details.

### Delete a Workout or Exercise

Use the appropriate DELETE endpoint with the record's ID. A successful deletion returns HTTP `204 No Content`; a missing record returns HTTP `404 Not Found`.

## Validation and Database Constraints

- Exercise names and categories cannot be empty.
- Workout duration must be positive.
- Repetitions, sets, and duration in seconds must be positive when provided.
- A workout cannot contain the same exercise more than once under the current database constraint.
- Marshmallow validates request data before the API creates database records.

Invalid request data returns HTTP `400 Bad Request`.

## Database Migrations

From the `server` directory, generate and apply migrations after changing the models:

```bash
flask db migrate -m "Describe the schema change"
flask db upgrade
```

The existing `migrations/` directory is committed to the repository; do not initialize it again.

## Development

Activate the virtual environment before running commands. Start the Flask server with `python app.py`, and use `curl` or an API client such as Postman to test the endpoints.
