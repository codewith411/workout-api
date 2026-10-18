
from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise


def seed_database():
    with app.app_context():
        # Clear existing records in dependency order.
        db.session.query(WorkoutExercise).delete()
        db.session.query(Workout).delete()
        db.session.query(Exercise).delete()
        db.session.commit()

        # Create exercises.
        pushups = Exercise(
            name="Push-ups",
            category="Strength",
            equipment_needed=False,
        )

        squats = Exercise(
            name="Squats",
            category="Strength",
            equipment_needed=False,
        )

        running = Exercise(
            name="Running",
            category="Cardio",
            equipment_needed=False,
        )

        db.session.add_all([pushups, squats, running])
        db.session.flush()

        # Create workouts.
        morning_workout = Workout(
            date=date(2026, 10, 18),
            duration_minutes=30,
            notes="Morning strength training",
        )

        cardio_workout = Workout(
            date=date(2026, 10, 17),
            duration_minutes=25,
            notes="Cardio session",
        )

        db.session.add_all([morning_workout, cardio_workout])
        db.session.flush()

        # Link exercises to workouts with training details.
        db.session.add_all([
            WorkoutExercise(
                workout_id=morning_workout.id,
                exercise_id=pushups.id,
                reps=12,
                sets=3,
                duration_seconds=60,
            ),
            WorkoutExercise(
                workout_id=morning_workout.id,
                exercise_id=squats.id,
                reps=15,
                sets=3,
                duration_seconds=90,
            ),
            WorkoutExercise(
                workout_id=cardio_workout.id,
                exercise_id=running.id,
                reps=None,
                sets=None,
                duration_seconds=1500,
            ),
        ])

        try:
            db.session.commit()
            print("Database seeded successfully!")
            print("Created 3 exercises, 2 workouts, and 3 workout-exercise records.")
        except Exception:
            db.session.rollback()
            raise


if __name__ == "__main__":
    seed_database()
