from flask import Blueprint

root = Blueprint(
    'root', __name__, template_folder='templates', static_folder='static')

from . import views
