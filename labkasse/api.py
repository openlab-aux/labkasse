from datetime import datetime

from flask.ext.restful import Resource, reqparse
from flask import redirect
from peewee import DoesNotExist

from labkasse import api
from labkasse.models import Item, Donation

class ItemsResource(Resource):
    def get(self):
        items = []
        for i in Item.select():
            items.append({
                'id': i.id,
                'name': i.name,
                'uri': i.uri,
                'max_count': i.max_count,
                'target': i.target,
                'max_count': i.max_count,
                'donation_sum': i.donation_sum
            })
        return items
        
api.add_resource(ItemsResource, '/api/items')
        
class SingleItemResource(Resource):
    @classmethod
    def _item_to_json(cls, item):
        return {
            'id': item.id,
            'name': item.name,
            'uri': item.uri,
            'max_count': item.max_count,
            'target': item.target,
            'max_count': item.max_count,
            'donation_sum': item.donation_sum,
            'sub_items': [ SingleItemResource._item_to_json(i) for i in 
                           list(item.sub_items) ]
        }

    def get(self, item_id):
        item = Item.select().where(Item.id == item_id).get()
        return SingleItemResource._item_to_json(item)
    
api.add_resource(SingleItemResource, '/api/items/<int:item_id>')

class DonationResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('item_id', type=int, required=True)
        parser.add_argument('value', type=float, required=True)
        args = parser.parse_args()
        
        try:
            item = Item.select().where(Item.id == args.item_id).get()
        except DoesNotExist:
            return {
                'message': "item does not not exist."
            }
        d = Donation.create(item=item,
                            value=args.value,
                            date = datetime.now())
        return redirect('/api/donations/%i' % d.id)
        
api.add_resource(DonationResource, '/api/donations')

class SingleDonationResource(Resource):
    def get(self, donation_id):
        donation = Donation.select().where(Donation.id == donation_id).get()
        return {
            'id': donation.id,
            'value': donation.value,
            'item_id': donation.item.id
        }

api.add_resource(SingleDonationResource, '/api/donations/<int:donation_id>')