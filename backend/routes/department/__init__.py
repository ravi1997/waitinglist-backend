from flask import Blueprint

bp = Blueprint('department', __name__)

from backend.routes.department import routes