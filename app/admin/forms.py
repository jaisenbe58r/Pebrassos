"""Copyright (c) 2020 Jaime Sendra Berenguer & Carlos Mahiques Ballester

Pebrassos - Machine Learning Library Extensions

Author:Jaime Sendra Berenguer & Carlos Mahiques Ballester  
<www.linkedin.com/in/jaisenbe>

License: MIT


FECHA DE CREACIÓN: 24/01/2019

"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, DateField, TextAreaField, BooleanField, SelectField)
from wtforms.validators import DataRequired, Length, Optional


class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    loc = StringField('Localidad', validators=[DataRequired(), Length(max=128)])
    state = SelectField("Estado", [Optional()], choices=[("0", "0"), ("2", "2"),
                                    ("4", "4"), ("6", "6"), ("8", "8"), ("10", "10")])
    date = DateField('Fecha', validators = [DataRequired(message="You need to enter the date.")], format='%d/%m/%Y')
    content = TextAreaField('Contenido')
    post_image = FileField('Imagen de cabecera', validators=[
        FileAllowed(['jpg', 'png'], 'Solo se permiten imágenes')
    ])
    submit = SubmitField('Guardar')


class UserAdminForm(FlaskForm):
    is_admin = BooleanField('Administrador')
    submit = SubmitField('Guardar')
