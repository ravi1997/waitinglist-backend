from backend.routes.user import bp
from flask_jwt_extended import get_jwt_identity,jwt_required
from flask import Flask,jsonify,request
from backend.models.user_model import Account,User
from backend.schemas.user_schemas import UserSchema
from marshmallow import ValidationError
import logging
from backend.extensions import db


@bp.route('/')
def index():
    return 'This is The waiting list user route'

@bp.route('/create',methods=["POST"])
@jwt_required()
def create_user():
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

    found_users = [obj for obj in current_user.AccountHasRoles if obj.name == "ADMIN"]

    if found_users:
        request_data = request.json
    
        if request_data is None:
            return jsonify({'message':'request data in not in valid format'}), 400
        
        schema = UserSchema()

        try:
            errors = schema.validate(request_data)
            if errors:
                return jsonify(errors), 400

            # Convert validated request schema into a User object
            user_data = schema.load(request_data)
            dp_name = user_data.fullname

            user = User.query.filter_by(fullname=user_data.fullname).first()
            if user is None:
                
                db.session.add(user_data)
                db.session.commit()
                logging.info("User is created : {dp_name}")
                return jsonify({"message":"User is created : {dp_name}"}), 200

            else:
                logging.info("User already : {dp_name}")
                return jsonify({"message":"User already : {dp_name}"}), 400

        except ValidationError as err:
            # Return a nice message if validation fails
            return jsonify(err.messages), 400

    else:
        return jsonify({"message":"User is not ADMIN"}),403
                

@bp.route('/getAll',methods=["GET"])
@jwt_required()
def getAll_user():
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

        
    schema = UserSchema(many=True)
    users = User.query.all()
    return schema.jsonify(users),200

@bp.route('/get/<id>',methods=["GET"])
@jwt_required()
def get_user(id):
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

        
    schema = UserSchema()
    user = User.query.filter_by(id=id).one_or_none()

    if user is None:
        return jsonify({"message":"User id doesnt exist"}),400

    return schema.jsonify(user),200

                
@bp.route('/update',methods=["PUT"])
@jwt_required()
def update_user():
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

    request_data = request.json
    
    if request_data is None:
        return jsonify({'message':'request data in not in valid format'}), 400
        
    schema = UserSchema()

    try:
        errors = schema.validate(request_data)
        if errors:
            return jsonify(errors), 400

        # Convert validated request schema into a User object
        user_data = schema.load(request_data)
        found_users = [obj for obj in current_user.AccountHasRoles if obj.name == "ADMIN"]

        if found_users is None:
            if user_data.id != current_user.user_id:
                return jsonify({"message":"The current user is not admin. Permission to change user data is allowed"}),403

        user = User.query.filter_by(id=user_data.id).first()
        if user is None:        
            return jsonify({"message":"User doesn't exist"}), 400
        else:
            user = user_data
            db.session.commit()
            return jsonify({"message":"User updated"}), 200

    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400
