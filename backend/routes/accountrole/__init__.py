from flask import Blueprint

bp = Blueprint('accountrole', __name__)

from backend.routes.accountrole import routes