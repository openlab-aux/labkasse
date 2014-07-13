from os.path import join, dirname

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask.ext.restful import Resource, Api
from flask_restful_swagger import swagger

app = Flask(__name__, 
            template_folder=join(dirname(__file__), '..', 'templates'),
            static_folder=join(dirname(__file__), '..', 'static')
)

import appconfig
app.config.from_object(appconfig)

db = SQLAlchemy(app)

from labkasse.models import *

admin = Admin(app)
admin.add_view(ModelView(Item, db.session))
admin.add_view(ModelView(Donation, db.session))

api = Api(app)
api = swagger.docs(api, api_spec_url='/api-docs')

import labkasse.api
import labkasse.views
