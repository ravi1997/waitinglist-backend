from flask import Blueprint

bp = Blueprint('unit', __name__)

from backend.routes.unit import routes