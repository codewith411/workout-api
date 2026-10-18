
from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100, error="Name must be 1–100 characters."),
    )

    category = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50, error="Category must be 1–50 characters."),
    )

    equipment_needed = fields.Bool(load_default=False)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)

    reps = fields.Int(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1, error="Reps must be at least 1."),
    )

    sets = fields.Int(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1, error="Sets must be at least 1."),
    )

    duration_seconds = fields.Int(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1, error="Duration must be at least 1 second."),
    )

    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1, error="Duration must be at least 1 minute."),
    )

    notes = fields.Str(allow_none=True, load_default=None)

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True,
    )

    @validates_schema
    def validate_workout(self, data, **kwargs):
        if data.get("notes") is not None and len(data["notes"]) > 2000:
            raise ValidationError(
                {"notes": ["Notes cannot exceed 2000 characters."]}
            )
