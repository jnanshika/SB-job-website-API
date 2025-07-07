from app.models import UserModel
from bcrypt import hashpw, checkpw, gensalt
from app.extensions import db
from datetime import timedelta
from flask_jwt_extended import create_access_token

class AuthService:
    @staticmethod
    def register_user(user):
        # Check if user already exists
        existing_user = UserModel.query.filter_by(email=user.email).first()
        if existing_user:
            return {"message": "An account already exists with this email!"}, 400
        
        hashed_password = hashpw(user.password.encode(), gensalt()).decode('utf-8')
        user.password = hashed_password
        try: 
            db.session.add(user) 
            db.session.commit()
        except:
            db.session.rollback()
            return {"error" : "Error occured while email registration"} , 400

        return {"message": "Email registered successfully"}, 201
    
    @staticmethod
    def login_user(user):
        db_user = UserModel.query.filter_by(email=user.email).first()
        if not db_user : 
            return {"error": "User not found!"}, 404
        
        #checkpw(plain password(user enter), encrypted password (database hashed password))
        if not checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
            return {"error": "Incorrect password!"}, 401
        
        # Create access token
        access_token = create_access_token(identity=str(db_user.id), expires_delta=timedelta(hours=1))
        return {"access_token": access_token}, 200