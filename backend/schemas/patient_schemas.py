from marshmallow import fields
from backend.extensions import ma
from backend.models.patient_model import Patient

class PatientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Patient
        include_fk = True
        include_relationships = True
        load_instance = True