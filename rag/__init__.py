from flask import Blueprint

bp = Blueprint('rag', __name__)

from . import routes
