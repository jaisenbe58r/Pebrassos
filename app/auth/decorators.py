"""Copyright (c) 2020 Jaime Sendra Berenguer & Carlos Mahiques Ballester

Pebrassos - Machine Learning Library Extensions

Author:Jaime Sendra Berenguer & Carlos Mahiques Ballester  
<www.linkedin.com/in/jaisenbe>

License: MIT


FECHA DE CREACIÓN: 13/01/2020

"""

from functools import wraps

from flask import abort

from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        is_admin = getattr(current_user, 'is_admin', False)
        if not is_admin:
            abort(401)
        return f(*args, **kws)
    return decorated_function
