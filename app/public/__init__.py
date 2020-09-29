"""
AUTOR: JAIME sENDRA

https://j2logo.com/tutorial-flask-leccion-17-desplegar-flask-produccion-nginx-gunicorn/


FECHA DE CREACIÓN: 24/05/2019

"""

from flask import Blueprint

public_bp = Blueprint('public', __name__, template_folder='templates')

from . import routes
