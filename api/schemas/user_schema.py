from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Usuario


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True
        include_fk = True
