from marshmallow import Schema, fields, validate


class UserSchema(Schema):

    username = fields.Str(
        required=True,
        validate=validate.Length(min=3)
    )

    password = fields.Str(
        required=True,
        validate=validate.Length(min=4)
    )



class ProjectSchema(Schema):

    name = fields.Str(
        required=True,
        validate=validate.Length(min=3)
    )



class TaskSchema(Schema):

    title = fields.Str(
        required=True,
        validate=validate.Length(min=3)
    )


    priority = fields.Str(
        validate=validate.OneOf(
            ["Low","Medium","High"]
        )
    )


    project_id = fields.Int(
        required=True
    )