from marshmallow import fields
from backend.extensions import ma
from backend.models.user_model import Department,Account,User,Cadre


class CadreSchema(ma.Schema):
    class Meta:
        model = Cadre
        include_fk = True
        include_relationships = True
        load_instance = True
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)


class DepartmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Department
        include_fk = True
        include_relationships = True
        load_instance = True
    id = fields.Number(dump_only=True)



class LoginAccoutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Account
        include_fk = True
        include_relationships = True
        load_instance = True
    
    username = fields.String(required=True)
    password = fields.String(required=True)


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        include_fk = True
        include_relationships = True
        load_instance = True
    id= fields.Number(dump_only=True)
    fullname = fields.String(required=True)

