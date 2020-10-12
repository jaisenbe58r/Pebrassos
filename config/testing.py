"""Copyright (c) 2020 Jaime Sendra Berenguer & Carlos Mahiques Ballester

Pebrassos - Machine Learning Library Extensions

Author:Jaime Sendra Berenguer & Carlos Mahiques Ballester  
<www.linkedin.com/in/jaisenbe>

License: MIT


FECHA DE CREACIÓN: 08/07/2019

"""

from .default import *


# Parámetros para activar el modo debug
TESTING = True
DEBUG = True

APP_ENV = APP_ENV_TESTING

WTF_CSRF_ENABLED = False

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://admin:1234@localhost:3307/Pebrassos_testing'

