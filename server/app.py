
from flask import Flask, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workout.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()


@app.route("/")
def home():
    return {"message": "Workout API is running!"}


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = db.session.query(Exercise).all()
    return exercises_schema.dump(exercises), 200


@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return {"error": "Exercise not found."}, 404

    return exercise_schema.dump(exercise), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json() or {})
    except ValidationError as error:
        return {"errors": error.messages}, 400

    exercise = Exercise(**data)
    db.session.add(exercise)

    try:
        db.session.commit()
    except (IntegrityError, ValueError) as error:
        db.session.rollback()
        return {"error": str(error)}, 400

    return exercise_schema.dump(exercise), 201


@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return {"error": "Exercise not found."}, 404

    db.session.delete(exercise)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Could not delete this exercise."}, 409

    return "", 204


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = db.session.query(Workout).all()
    return workouts_schema.dump(workouts), 200


@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return {"error": "Workout not found."}, 404

    return workout_schema.dump(workout), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    try:
        data = workout_schema.load(request.get_json() or {})
    except ValidationError as error:
        return {"errors": error.messages}, 400

    workout = Workout(
        date=data["date"],
        duration_minutes=data["duration_minutes"],
        notes=data.get("notes"),
    )

    db.session.add(workout)

    try:
        db.session.commit()
    except (IntegrityError, ValueError) as error:
        db.session.rollback()
        return {"error": str(error)}, 400

    return workout_schema.dump(workout), 201


@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return {"error": "Workout not found."}, 404

    db.session.delete(workout)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Could not delete this workout."}, 409

    return "", 204


@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"],
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if workout is None:
        return {"error": "Workout not found."}, 404

    if exercise is None:
        return {"error": "Exercise not found."}, 404

    try:
        data = workout_exercise_schema.load(request.get_json() or {})
    except ValidationError as error:
        return {"errors": error.messages}, 400

    workout_exercise = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        reps=data.get("reps"),
        sets=data.get("sets"),
        duration_seconds=data.get("duration_seconds"),
    )

    db.session.add(workout_exercise)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {
            "error": "This exercise may already be in the workout."
        }, 409
    except ValueError as error:
        db.session.rollback()
        return {"error": str(error)}, 400

    return workout_exercise_schema.dump(workout_exercise), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)
