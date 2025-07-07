from flask import Flask
from app.extensions import db, jwt 
from app.routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')  
    
    db.init_app(app)  
    
    register_routes(app)
    
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return 'Setup is ready!'  
    return app
