from flask import Flask
from app.routes import chatbot_bp   

def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecret"   
   
    app.register_blueprint(chatbot_bp)

    return app
