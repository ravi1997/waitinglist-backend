from flask import Blueprint

bp = Blueprint('role', __name__)

from backend.routes.role import routes