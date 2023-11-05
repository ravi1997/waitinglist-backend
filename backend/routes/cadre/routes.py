from backend.routes.cadre import bp
from flask_jwt_extended import get_jwt_identity,jwt_required
from flask import Flask,jsonify,request
from backend.models.user_model import Account,Cadre
from backend.schemas.user_schemas import CadreSchema
from marshmallow import ValidationError
import logging
from backend.extensions import db


@bp.route('/')
def index():
    return 'This is The waiting list cadre route'

@bp.route('/create',methods=["POST"])
@jwt_required()
def create_cadre():
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

    found_roles = [obj for obj in current_user.AccountHasRoles if obj.name == "ADMIN"]

    if found_roles:
        request_data = request.json
    
        if request_data is None:
            return jsonify({'message':'request data in not in valid format'}), 400
        
        schema = CadreSchema()

        try:
            errors = schema.validate(request_data)
            if errors:
                return jsonify(errors), 400

            # Convert validated request schema into a User object
            cadre_data = schema.load(request_data)
            dp_name = cadre_data.name

            cadre = Cadre.query.filter_by(name=cadre_data.name).first()
            if cadre is None:
                
                db.session.add(cadre_data)
                db.session.commit()
                logging.info("Cadre is created : {dp_name}")
                return jsonify({"message":"Cadre is created : {dp_name}"}), 200

            else:
                logging.info("Cadre already : {dp_name}")
                return jsonify({"message":"Cadre already : {dp_name}"}), 400

        except ValidationError as err:
            # Return a nice message if validation fails
            return jsonify(err.messages), 400

    else:
        return jsonify({"message":"User is not ADMIN"}),403
                

@bp.route('/getAll',methods=["GET"])
@jwt_required()
def getAll_cadre():
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

        
    schema = CadreSchema(many=True)
    users = Cadre.query.all()
    return schema.jsonify(users),200

@bp.route('/get/<id>',methods=["GET"])
@jwt_required()
def get_cadre(id):
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

        
    schema = CadreSchema()
    cadre = Cadre.query.filter_by(id=id).one_or_none()

    if cadre is None:
        return jsonify({"message":"Cadre id doesnt exist"}),400

    return schema.jsonify(cadre),200

                
@bp.route('/update',methods=["PUT"])
@jwt_required()
def update_cadre():
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

    found_roles = [obj for obj in current_user.AccountHasRoles if obj.name == "ADMIN"]

    if found_roles:
        request_data = request.json
    
        if request_data is None:
            return jsonify({'message':'request data in not in valid format'}), 400
        
        schema = CadreSchema()

        try:
            errors = schema.validate(request_data)
            if errors:
                return jsonify(errors), 400

            # Convert validated request schema into a User object
            cadre_data = schema.load(request_data)

            cadre = Cadre.query.filter_by(id=cadre_data.id).first()
            if cadre is None:        
                return jsonify({"message":"Cadre doesn't exist"}), 400
            else:
                cadre = cadre_data
                return jsonify({"message":"Cadre updated"}), 200

        except ValidationError as err:
            # Return a nice message if validation fails
            return jsonify(err.messages), 400

    else:
        return jsonify({"message":"User is not ADMIN"}),403
