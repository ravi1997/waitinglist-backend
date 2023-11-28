from backend.routes.accountrole import bp
from flask_jwt_extended import get_jwt_identity,jwt_required
from flask import Flask,jsonify,request
from backend.models.user_model import Account,AccountRole
from backend.schemas.user_schemas import AccountRoleSchema
from marshmallow import ValidationError
import logging
from backend.extensions import db


@bp.route('/')
def index():
    return 'This is The waiting list accountrole route'

@bp.route('/create',methods=["POST"])
@jwt_required()
def create_accountrole():
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

    found_accountroles = [obj for obj in current_user.AccountHasRoles if obj.name == "ADMIN"]

    if found_accountroles:
        request_data = request.json
    
        if request_data is None:
            return jsonify({'message':'request data in not in valid format'}), 400
        
        schema = AccountRoleSchema()

        try:
            errors = schema.validate(request_data)
            if errors:
                return jsonify(errors), 400

            # Convert validated request schema into a User object
            role_data = schema.load(request_data)

            accountrole = AccountRole.query.filter_by(account_id=role_data.account_id,role_id=role_data.role_id).first()
            if accountrole is None:
                
                db.session.add(role_data)
                db.session.commit()
                logging.info("AccountRole is created")
                return jsonify({"message":"AccountRole is created"}), 200

            else:
                logging.info("AccountRole already")
                return jsonify({"message":"AccountRole already"}), 400

        except ValidationError as err:
            return jsonify(err.messages), 400

    else:
        return jsonify({"message":"User is not ADMIN"}),403
                

@bp.route('/getAll',methods=["GET"])
@jwt_required()
def getAll_accountrole():
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

        
    schema = AccountRoleSchema(many=True)
    users = AccountRole.query.all()
    return schema.jsonify(users),200

@bp.route('/get/<id>',methods=["GET"])
@jwt_required()
def get_accountrole(id):
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

        
    schema = AccountRoleSchema(many=True)
    accountrole = AccountRole.query.filter_by(account_id=id)

    if accountrole is None:
        return jsonify({"message":"AccountRole id doesnt exist"}),400

    return schema.jsonify(accountrole),200

                
@bp.route('/update',methods=["PUT"])
@jwt_required()
def update_accountrole():
    current_user_id = get_jwt_identity()
    current_user = Account.query.filter_by(id=current_user_id).first()
    if current_user is None:
        return jsonify({"message":"User is not valid"}),401

    found_accountroles = [obj for obj in current_user.AccountHasRoles if obj.name == "ADMIN"]

    if found_accountroles:
        request_data = request.json
    
        if request_data is None:
            return jsonify({'message':'request data in not in valid format'}), 400
        
        schema = AccountRoleSchema()

        try:
            errors = schema.validate(request_data)
            if errors:
                return jsonify(errors), 400

            # Convert validated request schema into a User object
            role_data = schema.load(request_data)

            accountrole = AccountRole.query.filter_by(account_id=role_data.account_id,role_id=role_data.role_id).first()
            if accountrole is None:
                return jsonify({"message":"AccountRole doesn't exist"}), 400

            else:
                accountrole = role_data
                db.session.commit()
                return jsonify({"message":"AccountRole updated"}), 200

        except ValidationError as err:
            return jsonify(err.messages), 400

    else:
        return jsonify({"message":"User is not ADMIN"}),403
