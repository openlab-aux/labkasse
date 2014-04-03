from flask import Flask
from flask_peewee.db import Database
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
from flask.ext.restful import Resource, Api
from flask_restful_swagger import swagger

app = Flask(__name__)

import appconfig
app.config.from_object(appconfig)

db = Database(app)

from labkasse.models import *

admin = Admin(app)
admin.add_view(ModelView(Item))
admin.add_view(ModelView(Donation))

api = Api(app)
api = swagger.docs(api, api_spec_url='/api-docs')

import labkasse.api
