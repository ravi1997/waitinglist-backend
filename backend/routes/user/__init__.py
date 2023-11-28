from flask import Blueprint

bp = Blueprint('user', __name__)

from backend.routes.user import routes