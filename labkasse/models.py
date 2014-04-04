from datetime import datetime

from labkasse import app, db

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    max_count = db.Column(db.Integer)
    target = db.Column(db.Float)
    uri = db.Column(db.String)
    owner = db.Column(db.String)
    used_by = db.Column(db.String)
    location = db.Column(db.String)
    
    parent_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    parent = db.relationship("Item", remote_side='Item.id')

    donations = db.relationship('Donation', backref='item')
    
    def __repr__(self):
        return self.name
    
    @property
    def sub_items(self):
        return Item.query.filter(Item.parent_id == self.id).all()
    
    @property
    def donation_sum(self):
        sum = 0
        for d in self.donations:
            sum += d.value
        for i in self.sub_items:
            sum += i.donation_sum
            
        return sum
            

class Donation(db.Model):
    __tablename__ = 'donation'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    date = db.Column(db.DateTime)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
