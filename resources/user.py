from flask_restful import Resource,reqparse
from models.user import UserModel

class UserRegister(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=str,
		required=True,
		help="This field cannot be blank"
	)
	parser.add_argument('password',
		type=str,
		required=True,
		help="This field cannot be blank"
	)

	def post(self):
		data = UserRegister.parser.parse_args()
		user = UserModel.find_by_username(data['username'])
		if user:
			return {"message":"Username already exists!"}, 400
		else:
			try:
				new_user = UserModel(data['username'], data['password'])
				new_user.register_to_db()
				return {"message":"User created succesfully"}, 201
			except:
				return {"message":"error on register"}, 500
