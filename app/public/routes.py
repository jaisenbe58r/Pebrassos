"""Copyright (c) 2020 Jaime Sendra Berenguer & Carlos Mahiques Ballester

Pebrassos - Machine Learning Library Extensions

Author:Jaime Sendra Berenguer & Carlos Mahiques Ballester  
<www.linkedin.com/in/jaisenbe>

License: MIT


FECHA DE CREACIÓN: 24/05/2019

"""

import logging

from flask import abort, render_template, redirect, url_for, request, current_app
from flask_login import current_user

import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap

from app.models import Post, Comment
from . import public_bp
from .forms import CommentForm

logger = logging.getLogger(__name__)


@public_bp.route("/")
def index():
    logger.info('Mostrando los posts del blog')
    page = int(request.args.get('page', 1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    post_pagination = Post.all_paginated(page, per_page)
    return render_template("public/index.html", post_pagination=post_pagination)


@public_bp.route("/maps")
def map():
    # Read the data from the remote resource as DataFrame
    df = pd.read_csv("data/pueblos.csv", sep=";")
    # Calculate approximated center point for our map view
    center = [np.mean(df.Latitud.values), np.mean(df.Longitud.values)]
    # Setup our map
    map = folium.Map(location=center, zoom_start=6)
    # Setup our heatmap layer
    heatMap = HeatMap(zip(df.Latitud.values, df.Longitud.values),
                       min_opacity=0.1,
                       max_val=5,
                       radius=20, blur=4,
                       max_zoom=100)
    map.add_child(heatMap)
    return map._repr_html_()

@public_bp.route("/p/<string:slug>/", methods=['GET', 'POST'])
def show_post(slug):
    logger.info('Mostrando un post')
    logger.debug(f'Slug: {slug}')
    post = Post.get_by_slug(slug)
    if not post:
        logger.info(f'El post {slug} no existe')
        abort(404)
    form = CommentForm()
    if current_user.is_authenticated and form.validate_on_submit():
        content = form.content.data
        comment = Comment(content=content, user_id=current_user.id,
                          user_name=current_user.name, post_id=post.id)
        comment.save()
        return redirect(url_for('public.show_post', slug=post.title_slug))
    return render_template("public/post_view.html", post=post, form=form)


@public_bp.route("/error")
def show_error():
    res = 1 / 0
    posts = Post.get_all()
    return render_template("public/index.html", posts=posts)
