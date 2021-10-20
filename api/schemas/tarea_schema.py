from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Tarea


class TareaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tarea
        include_relationships = True
        load_instance = True
        include_fk = True
