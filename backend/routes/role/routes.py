from backend.routes.role import bp
from flask_jwt_extended import get_jwt_identity,jwt_required
from flask import Flask,jsonify,request
from backend.models.user_model import Account,Role
from backend.schemas.user_schemas import RoleSchema
from marshmallow import ValidationError
import logging
from backend.extensions import db


@bp.route('/')
def index():
    return 'This is The waiting list role route'

@bp.route('/create',methods=["POST"])
@jwt_required()
def create_role():
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

    found_roles = [obj for obj in current_user.AccountHasRoles if obj.name == "ADMIN"]

    if found_roles:
        request_data = request.json
    
        if request_data is None:
            return jsonify({'message':'request data in not in valid format'}), 400
        
        schema = RoleSchema()

        try:
            errors = schema.validate(request_data)
            if errors:
                return jsonify(errors), 400

            # Convert validated request schema into a User object
            role_data = schema.load(request_data)
            dp_name = role_data.name

            role = Role.query.filter_by(name=role_data.name).first()
            if role is None:
                
                db.session.add(role_data)
                db.session.commit()
                logging.info("Role is created : {dp_name}")
                return jsonify({"message":"Role is created : {dp_name}"}), 200

            else:
                logging.info("Role already : {dp_name}")
                return jsonify({"message":"Role already : {dp_name}"}), 400

        except ValidationError as err:
            # Return a nice message if validation fails
            return jsonify(err.messages), 400

    else:
        return jsonify({"message":"User is not ADMIN"}),403
                

@bp.route('/getAll',methods=["GET"])
@jwt_required()
def getAll_role():
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

        
    schema = RoleSchema(many=True)
    users = Role.query.all()
    return schema.jsonify(users),200

@bp.route('/get/<id>',methods=["GET"])
@jwt_required()
def get_role(id):
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

        
    schema = RoleSchema()
    role = Role.query.filter_by(id=id).one_or_none()

    if role is None:
        return jsonify({"message":"Role id doesnt exist"}),400

    return schema.jsonify(role),200

                
@bp.route('/update',methods=["PUT"])
@jwt_required()
def update_role():
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

    found_roles = [obj for obj in current_user.AccountHasRoles if obj.name == "ADMIN"]

    if found_roles:
        request_data = request.json
    
        if request_data is None:
            return jsonify({'message':'request data in not in valid format'}), 400
        
        schema = RoleSchema()

        try:
            errors = schema.validate(request_data)
            if errors:
                return jsonify(errors), 400

            # Convert validated request schema into a User object
            role_data = schema.load(request_data)

            role = Role.query.filter_by(id=role_data.id).first()
            if role is None:        
                return jsonify({"message":"Role doesn't exist"}), 400
            else:
                role = role_data
                db.session.commit()
                return jsonify({"message":"Role updated"}), 200

        except ValidationError as err:
            # Return a nice message if validation fails
            return jsonify(err.messages), 400

    else:
        return jsonify({"message":"User is not ADMIN"}),403
