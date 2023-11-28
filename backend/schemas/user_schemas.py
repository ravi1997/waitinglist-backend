from marshmallow import fields
from backend.extensions import ma
from backend.models.user_model import Department,Account,User , \
                                    Cadre, Role,AccountRole,    \
                                    Designation,Unit , UnitHead, DepartmentHead

class CadreSchema(ma.SQLAlchemyAutoSchema):
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


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        include_relationships = True
        load_instance = True
    id= fields.Number(dump_only=True)
    fullname = fields.String(required=True)


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        include_fk = True
        include_relationships = True
        load_instance = True
    id = fields.Number(dump_only=True)


class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Account
        include_fk = True
        include_relationships = True
        load_instance = True
    id= fields.Number(dump_only=True)


class AccountRoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AccountRole
        include_fk = True
        include_relationships = True
        load_instance = True

class UnitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Unit
        include_fk = True
        include_relationships = True
        load_instance = True
    id= fields.Number(dump_only=True)


class DesignationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Designation
        include_fk = True
        include_relationships = True
        load_instance = True
    id= fields.Number(dump_only=True)


class UnitHeadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UnitHead
        include_fk = True
        include_relationships = True
        load_instance = True
    id= fields.Number(dump_only=True)



class DepartmentHeadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DepartmentHead
        include_fk = True
        include_relationships = True
        load_instance = True
    id= fields.Number(dump_only=True)