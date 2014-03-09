from flask import Flask
from flask_peewee.db import Database
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
from flask.ext.restful import Resource, Api

app = Flask(__name__)

import appconfig
app.config.from_object(appconfig)

db = Database(app)

from labkasse.models import *

admin = Admin(app)
admin.add_view(ModelView(Item))
admin.add_view(ModelView(Donation))

api = Api(app)

import labkasse.api
