
from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    __table_args__ = (
        CheckConstraint(
            "duration_minutes > 0",
            name="ck_workout_duration_positive",
        ),
    )

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan",
    )

    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        viewonly=True,
    )

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError("Workout duration must be a positive integer.")
        return value


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )

    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        viewonly=True,
    )

    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Exercise name cannot be empty.")
        if len(value.strip()) > 100:
            raise ValueError("Exercise name cannot exceed 100 characters.")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Exercise category cannot be empty.")
        if len(value.strip()) > 50:
            raise ValueError("Exercise category cannot exceed 50 characters.")
        return value.strip()


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id"),
        nullable=False,
    )
    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id"),
        nullable=False,
    )

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    __table_args__ = (
        UniqueConstraint(
            "workout_id",
            "exercise_id",
            name="uq_workout_exercise",
        ),
        CheckConstraint(
            "reps IS NULL OR reps > 0",
            name="ck_workout_exercise_reps_positive",
        ),
        CheckConstraint(
            "sets IS NULL OR sets > 0",
            name="ck_workout_exercise_sets_positive",
        ),
        CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds > 0",
            name="ck_workout_exercise_duration_positive",
        ),
    )

    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises",
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises",
    )

    @validates("reps", "sets", "duration_seconds")
    def validate_exercise_details(self, key, value):
        if value is not None:
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise ValueError(f"{key} must be a positive integer.")
        return value
