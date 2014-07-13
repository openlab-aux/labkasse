from datetime import datetime

from flask.ext.restful import Resource, reqparse
from sqlalchemy.orm.exc import NoResultFound

from labkasse import api, db
from labkasse.models import Item, Donation


class ItemsResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('search', type=str, required=False)
        args = parser.parse_args()
        
        if args.search is not None:
            items = Item.query.filter(Item.name.contains(args.search)).all()
        else:
            items = Item.query.all()
            
            
        res = []
        for i in items:
            res.append({
                'id': i.id,
                'name': i.name,
                'owner': i.owner,
                'used_by': i.used_by,
                'location': i.location,
                'uri': i.uri,
                'max_count': i.max_count,
                'target': i.target,
                'max_count': i.max_count,
                'donation_sum': i.donation_sum
            })

        return res
        
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('owner', type=str, required=False)
        parser.add_argument('uri', type=str, required=False)
        parser.add_argument('parent_id', type=int, required=False)
        parser.add_argument('target', type=float, required=False)
        parser.add_argument('max_count', type=int, required=False)
        
        args = parser.parse_args()
        
        if args.parent_id is not None:
            try:
                parent = Item.query.filter(Item.id == args.parent_id).one()
            except NoResultFound:
                return {
                    "message": "Parent item does not exist"
                }
        else:
            parent = None

        i = Item()
        i.name = args.name
        i.owner = args.owner
        i.uri = args.uri
        i.parent = parent
        i.target = args.target
        i.max_count = args.max_count
        
        db.session.add(i)
        db.session.commit()
        
        return SingleItemResource._item_to_json(i), 201

api.add_resource(ItemsResource, '/api/items')
        
class SingleItemResource(Resource):
    @classmethod
    def _item_to_json(cls, item):
        return {
            'id': item.id,
            'name': item.name,
            'owner': item.owner,
            'used_by': item.used_by,
            'location': item.location,
            'uri': item.uri,
            'max_count': item.max_count,
            'target': item.target,
            'max_count': item.max_count,
            'donation_sum': item.donation_sum,
            'sub_items': [ SingleItemResource._item_to_json(i) for i in 
                           list(item.sub_items) ]
        }

    def get(self, item_id):
        try:
            item = Item.query.filter(Item.id == item_id).one()
        except NoResultFound:
            return {
                "message": "Item not found"
            }, 404
        return SingleItemResource._item_to_json(item)
    
    def put(self, item_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=False)
        parser.add_argument('owner', type=str, required=False)
        parser.add_argument('used_by', type=str, required=False)
        parser.add_argument('location', type=str, required=False)
        parser.add_argument('uri', type=str, required=False)
        parser.add_argument('parent_id', type=int, required=False)
        parser.add_argument('target', type=float, required=False)
        parser.add_argument('max_count', type=int, required=False)
        
        args = parser.parse_args()
        
        try:
            i = Item.query.filter(Item.id == item_id).one()
        except NoResultFound:
            return {
                "message": "Item not found",
            }, 400
        
        if args.name is not None:
            i.name = args.name
        if args.owner is not None:
            i.owner = args.owner
        if args.used_by is not None:
            i.used_by = args.used_by
        if args.location is not None:
            i.location = args.location
        if args.uri is not None:
            i.uri = args.uri
        if args.parent_id is not None:
            try:
                parent = Item.select().where(Item.id == args.parent_id)
            except DoesNotExist:
                return {
                    "message": "Parent Item does not exist"
                }
            i.parent = parent
        if args.target is not None:
            i.target = args.target
        if args.max_count is not None:
            i.max_count = args.max_count
            
        db.session.commit()

        return SingleItemResource._item_to_json(i), 201

api.add_resource(SingleItemResource, '/api/items/<int:item_id>')

class DonationResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('item_id', type=int, required=True)
        parser.add_argument('value', type=float, required=True)
        args = parser.parse_args()
        
        try:
            item = Item.query.filter(Item.id == args.item_id).one()
        except NoResultFound:
            return {
                'message': "Item does not not exist."
            }
        d = Donation()

        d.item=item
        d.value=args.value
        d.date = datetime.now()
        
        db.session.add(d)
        db.session.commit()

        return SingleDonationResource().get(d.id), 201
        
api.add_resource(DonationResource, '/api/donations')

class SingleDonationResource(Resource):
    def get(self, donation_id):
        try:
            donation = Donation.query.filter(Donation.id == donation_id).one()
        except NoResultFound:
            return {
                'message': "Donation not found"
            }, 404
        return {
            'id': donation.id,
            'value': donation.value,
            'item_id': donation.item.id
        }

api.add_resource(SingleDonationResource, '/api/donations/<int:donation_id>')
