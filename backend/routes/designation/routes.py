from backend.routes.designation import bp
from flask_jwt_extended import get_jwt_identity,jwt_required
from flask import Flask,jsonify,request
from backend.models.user_model import Account,Designation
from backend.schemas.user_schemas import DesignationSchema
from marshmallow import ValidationError
import logging
from backend.extensions import db


@bp.route('/')
def index():
    return 'This is The waiting list designation route'

@bp.route('/create',methods=["POST"])
@jwt_required()
def create_designation():
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

    found_roles = [obj for obj in current_user.AccountHasRoles if obj.name == "ADMIN"]

    if found_roles:
        request_data = request.json
    
        if request_data is None:
            return jsonify({'message':'request data in not in valid format'}), 400
        
        schema = DesignationSchema()

        try:
            errors = schema.validate(request_data)
            if errors:
                return jsonify(errors), 400

            # Convert validated request schema into a User object
            unit_data = schema.load(request_data)
            dp_name = unit_data.name

            designation = Designation.query.filter_by(name=unit_data.name).first()
            if designation is None:
                
                db.session.add(unit_data)
                db.session.commit()
                logging.info("Designation is created : {dp_name}")
                return jsonify({"message":"Designation is created : {dp_name}"}), 200

            else:
                logging.info("Designation already : {dp_name}")
                return jsonify({"message":"Designation already : {dp_name}"}), 400

        except ValidationError as err:
            # Return a nice message if validation fails
            return jsonify(err.messages), 400

    else:
        return jsonify({"message":"User is not ADMIN"}),403
                

@bp.route('/getAll',methods=["GET"])
@jwt_required()
def getAll_designation():
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

        
    schema = DesignationSchema(many=True)
    users = Designation.query.all()
    return schema.jsonify(users),200

@bp.route('/get/<id>',methods=["GET"])
@jwt_required()
def get_designation(id):
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

        
    schema = DesignationSchema()
    designation = Designation.query.filter_by(id=id).one_or_none()

    if designation is None:
        return jsonify({"message":"Designation id doesnt exist"}),400

    return schema.jsonify(designation),200

                
@bp.route('/update',methods=["PUT"])
@jwt_required()
def update_designation():
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

    found_roles = [obj for obj in current_user.AccountHasRoles if obj.name == "ADMIN"]

    if found_roles:
        request_data = request.json
    
        if request_data is None:
            return jsonify({'message':'request data in not in valid format'}), 400
        
        schema = DesignationSchema()

        try:
            errors = schema.validate(request_data)
            if errors:
                return jsonify(errors), 400

            # Convert validated request schema into a User object
            unit_data = schema.load(request_data)

            designation = Designation.query.filter_by(id=unit_data.id).first()
            if designation is None:        
                return jsonify({"message":"Designation doesn't exist"}), 400
            else:
                designation = unit_data
                db.session.commit()
                return jsonify({"message":"Designation updated"}), 200

        except ValidationError as err:
            # Return a nice message if validation fails
            return jsonify(err.messages), 400

    else:
        return jsonify({"message":"User is not ADMIN"}),403
