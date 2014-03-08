from datetime import datetime

from labkasse import app, db

from peewee import TextField, IntegerField, FloatField, BooleanField, \
    ForeignKeyField, DateTimeField

class Item(db.Model):
    name = TextField()
    max_count = IntegerField(null=True)
    target = FloatField(null=True)
    uri = TextField(null=True)

    parent = ForeignKeyField('self', related_name='sub_items', null=True)
    
    def __unicode__(self):
        return self.name

    @property
    def sub_items(self):
        return list(Item.select().where(Item.parent == self))

class Donation(db.Model):
    value = FloatField()
    date = DateTimeField(default=datetime.now)
    item = ForeignKeyField(Item, related_name='donations')
