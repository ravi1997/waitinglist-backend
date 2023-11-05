from flask import Blueprint

bp = Blueprint('patient', __name__)

from backend.routes.patient import routes