from backend.routes.department import bp
from flask_jwt_extended import get_jwt_identity,jwt_required
from flask import Flask,jsonify,request
from backend.models.user_model import Account,Department
from backend.schemas.user_schemas import DepartmentSchema
from marshmallow import ValidationError
import logging
from backend.extensions import db


@bp.route('/')
def index():
    return 'This is The waiting list department route'

@bp.route('/create',methods=["POST"])
@jwt_required()
def create_department():
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

    found_roles = [obj for obj in current_user.AccountHasRoles if obj.name == "ADMIN"]

    if found_roles:
        request_data = request.json
    
        if request_data is None:
            return jsonify({'message':'request data in not in valid format'}), 400
        
        schema = DepartmentSchema()

        try:
            errors = schema.validate(request_data)
            if errors:
                return jsonify(errors), 400

            # Convert validated request schema into a User object
            department_data = schema.load(request_data)
            dp_name = department_data.name

            department = Department.query.filter_by(name=department_data.name).first()
            if department is None:
                
                db.session.add(department_data)
                db.session.commit()
                logging.info("Department is created : {dp_name}")
                return jsonify({"message":"Department is created : {dp_name}"}), 200

            else:
                logging.info("Department already : {dp_name}")
                return jsonify({"message":"Department already : {dp_name}"}), 400

        except ValidationError as err:
            # Return a nice message if validation fails
            return jsonify(err.messages), 400

    else:
        return jsonify({"message":"User is not ADMIN"}),403
                

@bp.route('/getAll',methods=["GET"])
@jwt_required()
def getAll_department():
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

        
    schema = DepartmentSchema(many=True)
    users = Department.query.all()
    return schema.jsonify(users),200

@bp.route('/get/<id>',methods=["GET"])
@jwt_required()
def get_department(id):
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

        
    schema = DepartmentSchema()
    department = Department.query.filter_by(id=id).one_or_none()

    if department is None:
        return jsonify({"message":"Department id doesnt exist"}),400

    return schema.jsonify(department),200

                
@bp.route('/update',methods=["PUT"])
@jwt_required()
def update_department():
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

    found_roles = [obj for obj in current_user.AccountHasRoles if obj.name == "ADMIN"]

    if found_roles:
        request_data = request.json
    
        if request_data is None:
            return jsonify({'message':'request data in not in valid format'}), 400
        
        schema = DepartmentSchema()

        try:
            errors = schema.validate(request_data)
            if errors:
                return jsonify(errors), 400

            # Convert validated request schema into a User object
            department_data = schema.load(request_data)

            department = Department.query.filter_by(id=department_data.id).first()
            if department is None:        
                return jsonify({"message":"Department doesn't exist"}), 400
            else:
                department = department_data
                return jsonify({"message":"Department updated"}), 200

        except ValidationError as err:
            # Return a nice message if validation fails
            return jsonify(err.messages), 400

    else:
        return jsonify({"message":"User is not ADMIN"}),403
