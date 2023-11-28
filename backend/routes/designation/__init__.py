from flask import Blueprint

bp = Blueprint('designation', __name__)

from backend.routes.designation import routes