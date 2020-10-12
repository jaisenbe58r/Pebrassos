"""Copyright (c) 2020 Jaime Sendra Berenguer & Carlos Mahiques Ballester

Pebrassos - Machine Learning Library Extensions

Author:Jaime Sendra Berenguer & Carlos Mahiques Ballester  
<www.linkedin.com/in/jaisenbe>

License: MIT


FECHA DE CREACIÓN: 15/02/2019

"""

import logging
import datetime

from slugify import slugify
from sqlalchemy.exc import IntegrityError

from app import db

logger = logging.getLogger(__name__)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    title_slug = db.Column(db.String(256), unique=True, nullable=False)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    loc = db.Column(db.Text)
    state = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    image_name = db.Column(db.String(256))
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan',
                               order_by='asc(Comment.created)')

    def __repr__(self):
        return f'<Post {self.title}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        if not self.title_slug:
            self.title_slug = slugify(self.title)

        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                db.session.rollback()
                db.session.add(self)
                count += 1
                self.title_slug = f'{slugify(self.title)}-{count}'

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_slug(slug):
        return Post.query.filter_by(title_slug=slug).first()

    @staticmethod
    def get_by_id(id):
        return Post.query.get(id)

    @staticmethod
    def get_all():
        return Post.query.all()

    @staticmethod
    def all_paginated(page=1, per_page=20):
        return Post.query.order_by(Post.created.asc()). \
            paginate(page=page, per_page=per_page, error_out=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id', ondelete='SET NULL'))
    user_name = db.Column(db.String(50))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, content, user_id=None, user_name=user_name, post_id=None):
        self.content = content
        self.user_id = user_id
        self.user_name = user_name
        self.post_id = post_id

    def __repr__(self):
        return f'<Comment {self.content}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_post_id(post_id):
        return Comment.query.filter_by(post_id=post_id).all()


class WeatherStation(db.Model):
    station_id = db.Column(db.String(8), nullable=False, primary_key=True)
    municipio = db.Column(db.String(80), nullable=False)
    municipio_slug = db.Column(db.String(80), unique=True, nullable=False)
    provincia = db.Column(db.String(80), nullable=False)
    altura = db.Column(db.Integer, nullable=False)
    latitud = db.Column(db.String(8))
    latitud_gd = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.String(8))
    longitud_gd = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Weather Station {self.station_id}>'

    def save(self):
        # if not self.station_id:
        logger.info("Add in Database")
        db.session.add(self)
        if not self.municipio_slug:
            self.municipio_slug = slugify(self.municipio)
            logger.info(f'municipio_slug: {self.municipio_slug}')

        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                db.session.rollback()
                db.session.add(self)
                count += 1
                self.municipio_slug = f'{slugify(self.municipio)}-{count}'

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_slug(slug):
        return WeatherStation.query.filter_by(municipio_slug=slug).first()

    @staticmethod
    def get_by_station(station_id):
        return WeatherStation.query.get(station_id)

    @staticmethod
    def get_all():
        return WeatherStation.query.all()

    @staticmethod
    def all_paginated(page=1, per_page=20):
        return WeatherStation.query.order_by(WeatherStation.municipio_slug.asc()). \
            paginate(page=page, per_page=per_page, error_out=False)


class HistWeatherStatiion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String(8), db.ForeignKey('weather_station.station_id', ondelete='SET NULL'))
    reception_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    Location_name = db.Column(db.String(80), nullable=False)
    Location_name_slug = db.Column(db.String(80), nullable=False)
    Location_lon = db.Column(db.Float, nullable=False)
    Location_lat = db.Column(db.Float, nullable=False)
    id_loc = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(20), nullable=False)
    reference_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    sunset_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    sunrise_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    clouds = db.Column(db.Integer)
    rain = db.Column(db.String(20))
    wind_speed = db.Column(db.Float)
    wind_deg = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    pressure = db.Column(db.Integer)
    sea_level = db.Column(db.Float)
    temp = db.Column(db.Float)
    temp_kf = db.Column(db.Float)
    temp_max = db.Column(db.Float)
    temp_min = db.Column(db.Float)
    status = db.Column(db.String(20))
    detailed_status = db.Column(db.String(80))
    weather_code = db.Column(db.Integer)
    weather_icon_name = db.Column(db.String(20))
    visibility_distance = db.Column(db.Integer)
    dewpoint = db.Column(db.Float)
    humidex = db.Column(db.Float)
    heat_index = db.Column(db.Float)

    def __repr__(self):
        return f'<Weather Station {self.station_id}>'

    def save(self):
        # if not self.station_id:
        logger.info("Add in Database")
        db.session.add(self)
        if not self.Location_name_slug:
            self.Location_name_slug = slugify(self.Location_name)
            logger.info(f'municipio_slug: {self.Location_name_slug}')

        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                db.session.rollback()
                db.session.add(self)
                count += 1
                self.Location_name_slug = f'{slugify(self.Location_name)}-{count}'

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_slug(slug):
        return HistWeatherStatiion.query.filter_by(Location_name_slug=slug).first()

    @staticmethod
    def get_by_station(station_id):
        return HistWeatherStatiion.query.get(station_id)

    @staticmethod
    def get_all():
        return HistWeatherStatiion.query.all()

    @staticmethod
    def all_paginated(page=1, per_page=20):
        return HistWeatherStatiion.query.order_by(HistWeatherStatiion.Location_name_slug.asc()). \
            paginate(page=page, per_page=per_page, error_out=False)
