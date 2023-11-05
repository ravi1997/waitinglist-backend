from backend.routes.patient import bp
from backend.models.patient_model import Patient
from backend.schemas.patient_schemas import PatientSchema
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from flask import Flask,jsonify,request
from backend.util import to_date

from marshmallow import ValidationError
from backend.extensions import db



@bp.route('/')
def index():
	return 'This is The waiting list answer route'

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@bp.route("/CU", methods=["POST","PUT"])
@jwt_required()
def CUPatient():
	# Access the identity of the current user with get_jwt_identity
	current_user = get_jwt_identity()

	request_data = request.json
	
	if request_data is None:
		return jsonify({'message':'request data in not in valid format'}), 400
	
	schema = PatientSchema()

	try:
		errors = schema.validate(request_data)
		if errors:
			return jsonify(errors), 400

		# Convert validated request schema into a User object
		patient_data = schema.load(request_data)


		if patient_data.id is not None:
			patient = Patient.query.filter_by(id = patient_data.id).one_or_none()
			if patient is None and request.method == 'PUT':
				return jsonify({'message': 'patient is not found.'}), 404
			elif request.method == 'PUT':
				return jsonify({'message': 'patient is not found.'}), 404
			patient = patient_data
			db.session.commit()
		else:
			db.session.add(patient_data)
			db.session.commit()
		return jsonify(message="Successfull",patient = schema.dump(patient_data)),200
	except ValidationError as err:
		# Return a nice message if validation fails
		return jsonify(err.messages), 400


@bp.route("/redate/<id>", methods=["PUT"])
@jwt_required()
def redate(id):
	# Access the identity of the current user with get_jwt_identity
	current_user = get_jwt_identity()

	request_data = request.json
	
	if request_data is None:
		return jsonify({'message':'request data in not in valid format'}), 400
	
	try:
		if id is not None:
			patient = Patient.query.filter_by(id = id).one_or_none()
			if patient is None:
				return jsonify({'message': 'patient is not found.'}), 404
			patient.finalDate = to_date(request_data['date'])
			db.session.commit()
		else:
			return jsonify({'message': 'patient id is not found.'}), 404
		return jsonify(message="Successfull",patient = schema.dump(patient_data)),200
	except ValidationError as err:
		# Return a nice message if validation fails
		return jsonify(err.messages), 400



@bp.route("/<id>", methods=["GET"])
@jwt_required()
def getPatient(id):
	# Access the identity of the current user with get_jwt_identity
	current_user = get_jwt_identity()

	schema = PatientSchema()
	
	try:
		if id is not None:
			patient = Patient.query.filter_by(id = id).one_or_none()
			if patient is None:
				return jsonify({'message': 'patient is not found.'}), 404
			return jsonify(message="Successfull",patient = schema.dump(patient)),200
		else:
			return jsonify({'message': 'patient id is not found.'}), 404
	except ValidationError as err:
		# Return a nice message if validation fails
		return jsonify(err.messages), 400



@bp.route("/getAll", methods=["GET"])
@jwt_required()
def getAllPatient():
	# Access the identity of the current user with get_jwt_identity
	current_user = get_jwt_identity()

	schema = PatientSchema(many=True)
	
	try:
			patient = Patient.query.all()
			if patient is None:
				return jsonify({'message': 'patient is not found.'}), 404
			return jsonify(message="Successfull",patient = schema.dump(patient)),200
	except ValidationError as err:
		# Return a nice message if validation fails
		return jsonify(err.messages), 400



@bp.route("/<id>", methods=["DELETE"])
@jwt_required()
def deletePatient(id):
	# Access the identity of the current user with get_jwt_identity
	current_user = get_jwt_identity()

	if id is not None:
		patient = Patient.query.filter_by(id = id).one_or_none()
		if patient is None:
			return jsonify({'message': 'patient is not found.'}), 404
		db.session.delete(patient)
		db.session.commit()
		return jsonify(message="Successfull"),200
	else:
		return jsonify({'message': 'patient id is not found.'}), 404

