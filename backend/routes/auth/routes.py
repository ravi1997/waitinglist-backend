from backend.routes.auth import bp
from backend.models.user_model import Account
from backend.schemas.user_schemas import LoginAccoutSchema,UserSchema
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from flask import Flask,jsonify,request

from marshmallow import ValidationError

@bp.route('/')
def index():
    return 'This is The waiting list auth route'


@bp.route("/login", methods=["POST"])
def login():
    request_data = request.json
    
    if request_data is None:
        return jsonify({'message':'request data in not in valid format'}), 400
    
    schema = LoginAccoutSchema()
    user_schema = UserSchema()

    try:
        errors = schema.validate(request_data)
        if errors:
            return jsonify(errors), 400

        # Convert validated request schema into a User object
        useraccount_data = schema.load(request_data)

        userAccount = Account.query.filter_by(username=useraccount_data.username).one_or_none()
        if not userAccount or not userAccount.check_password(useraccount_data.password):
            return jsonify("Wrong username or password"), 401

        access_token = create_access_token(identity=userAccount.id)
        return jsonify(access_token=access_token,user=user_schema.dump(userAccount.accountBelongsToUser))
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400






# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@bp.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200