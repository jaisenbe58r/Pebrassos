"""
AUTOR: JAIME sENDRA

https://j2logo.com/tutorial-flask-leccion-17-desplegar-flask-produccion-nginx-gunicorn/


FECHA DE CREACIÓN: 08/07/2019

"""
from .default import *


SECRET_KEY = '5e04a4955d8878191923e86fe6a0dfb24edb226c87d6c7787f35ba4698afc86e95cae409aebd47f7'

APP_ENV = APP_ENV_PRODUCTION

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://admin:1234@localhost:3307/mminiblog'