# -*- coding: utf-8 -*-
#
# This file is part of Zenodo.
# Copyright (C) 2015 CERN.
#
# Zenodo is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Zenodo is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zenodo; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Zenodo frontpage blueprint."""

from __future__ import absolute_import, print_function

from flask import Blueprint, render_template
from flask import Response, json, current_app
from flask_babelex import lazy_gettext as _
from flask_menu import current_menu

from ...modules.cache.pages import cached
from .api import FrontpageRecordsSearch

import requests
import datetime

blueprint = Blueprint(
    'zenodo_frontpage',
    __name__,
    url_prefix='',
    template_folder='templates',
)


@blueprint.before_app_first_request
def init_menu():
    """Initialize menu before first request."""
    item = current_menu.submenu('main.deposit')
    item.register(
        'invenio_deposit_ui.index',
        _('Upload'),
        order=2,
    )
    item = current_menu.submenu('main.communities')
    item.register(
        'invenio_communities.index',
        _('Communities'),
        order=3,
    )


@blueprint.route('/')
@cached(timeout=600, key_prefix='frontpage')
def index():
    """Frontpage blueprint."""
    return render_template(
        'zenodo_frontpage/index.html',
        records=FrontpageRecordsSearch()[:10].sort('-_created').execute(),
    )


@blueprint.route('/ping', methods=['HEAD', 'GET'])
def ping():
    """Load balancer ping view."""
    return 'OK'


@blueprint.route('/padron')
#@cached(timeout=600, key_prefix='frontpage')
def padron():
    """Base information"""
    
    class Persona(object):
        def __init__(self, correo, nombre, tel, pApellido, sApellido):
            self.correo = correo
            self.nombre = nombre
            self.tel = tel
            self.pApellido = pApellido
            self.sApellido = sApellido

    personas = [
        Persona("agmartinez@inmegen.gob.mx", "Alejandro", "525553501900", "Martinez", "Romero")]
    depositarios = []
    for persona in personas:
        depositarios.append({
            "correo": persona.correo,
            "nombre": persona.nombre,
            "numTel": persona.tel,
            "pApellido": persona.pApellido,
            "sApellido": persona.sApellido})

    return Response(
        json.dumps({"depositarios": depositarios}), 
        mimetype='application/json'
    )


@blueprint.route('/raking/articulos')
def raking_articulos():
    """Base information"""

    today = datetime.date.today().strftime("%Y-%m-%d")
    url = "http://estadisticas.inmegen.gob.mx/index.php?module=API&method=Actions.getPageUrls&idSite=9&period=range&date=2017-06-30,{today}&format=JSON&token_auth={token}&expanded=0&flat=1&filter_limit=15&filter_pattern_recursive=record/*".format(token=current_app.config["TOKEN_AUTH_PIWIK"], today=today)
    r = requests.get(url)
    data = r.json()
    articulos = []
    for record in data:
        articulos.append({
            "id": record["url"],
            "numero": record["nb_hits"]
        })

    return Response(
        json.dumps({"articulos": articulos}), 
        mimetype='application/json'
    )


@blueprint.route('/descargas')
def descargas():
    """Base information"""

    today = datetime.date.today().strftime("%Y-%m-%d")
    url = "http://estadisticas.inmegen.gob.mx/index.php?module=API&method=Actions.getDownloads&idSite=9&period=range&date=2017-06-30,{today}&filter_limit=15&format=JSON&token_auth={token}".format(token=current_app.config["TOKEN_AUTH_PIWIK"], today=today)
    r = requests.get(url)
    data = r.json()
    descargas = []
    for record in data:
        articulos.append({
            "id": record["url"],
            "numero": record["nb_hits"]
        })

    return Response(
        json.dumps({"descargas": descargas}), 
        mimetype='application/json'
    )


@blueprint.route('/ranking/autores')
def autores():
    """Base information"""

    return Response(
        json.dumps({"autores": []}), 
        mimetype='application/json'
    )

