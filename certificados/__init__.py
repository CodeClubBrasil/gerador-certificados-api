from flask import Blueprint

certificados_bp = Blueprint('certificados', __name__)

from . import views
