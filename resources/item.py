from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price',
		type=float,
		required=True,
		help="This field cannot be left blank!"
		)
	parser.add_argument('store_id',
		type=int,
		required=True,
		help="Every item needs a store id."
		)
		 
	@jwt_required()
	def get(self,name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {"mesage":"item not found!"},404


	def post(self,name):
		data = Item.parser.parse_args()

		new_item = ItemModel(name, data['price'], data['store_id'])

		if ItemModel.find_by_name(name):
			return {'message': "An item with name '{}' already exists".format(name)}, 400
		else:
			try:
				new_item.save_to_db()
			except:
				return {"message":"Error occured while inserting the item."}, 500 #internal Server Error

		return new_item.json(), 201


	def delete(self,name):
		item = Item.find_by_name(name)
		if item:
			item.delete_from_db()

		return {"message":"Item was deleted."}

	def put(self,name):

			data = Item.parser.parse_args()

			item = ItemModel.find_by_name(name)

			if item is None:
				item = ItemModel(name, data['price'], data['store_id'])
			else:
				item.price = data['price']
				item.store_id = data['store_id']

			item.save_to_db()

			return item.json()


class ItemList(Resource):
	def get(self):
		return {'items': [item.json() for item in ItemModel.query.all()]}
