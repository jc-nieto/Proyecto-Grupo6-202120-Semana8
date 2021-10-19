from marshmallow import fields

from ext import marshmallow


class TaskSchema(marshmallow.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
