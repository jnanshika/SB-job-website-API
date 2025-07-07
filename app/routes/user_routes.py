from flask import Blueprint, jsonify, request
from app.services import AuthService
from app.models import UserModel
from app.schemas import VALID_ROLES, ValidationError, UserSchema
from app.extensions import db
from app.utils import token_required, candidate_required

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['POST'])
def register():
    jsondata = request.get_json()

    try:
        user_schema = UserSchema(session =db.session)
        user = user_schema.load(jsondata)  
    
    except ValidationError as error:
        return {"errors": error.messages}, 400
    
    if user.role not in VALID_ROLES:
        return jsonify({"error": "Invalid role provided"}), 400
    
    return AuthService.register_user(user)

@user_routes.route('/login', methods=['POST'])
def login():
    jsondata = request.get_json()
    email = jsondata.get('email')
    password = jsondata.get('password')

    if not email or not password:
        return {"error": "Email and password are required and cannot be empty."}, 400

    try:
        user_schema = UserSchema(session =db.session)
        user = user_schema.load(jsondata, partial =True)  
    except ValidationError as error:
        return {"errors": error.messages}, 400
    
    return AuthService.login_user(user)

@user_routes.route('/', methods=['GET'])
def get_all_users():
    users = UserModel.query.all()
    if not users:
        return {"message": "No user found"}, 200
    
    try: 
        user_schema = UserSchema(many= True)
        if not users:
            return {"message": "No users found"}, 40
        return {"users": user_schema.dump(users.items)}, 200
    
    except Exception as e:
        return {"error": f"Unexpected error occurred while retrieving user information: {str(e)}"}, 500
