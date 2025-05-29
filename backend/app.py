from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from flask_cors import CORS


app= Flask(__name__)
CORS(app)
app.config.from_object(Config)

db= SQLAlchemy(app)
jwt= JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()

from routes import *

#if __name__ == '__main__':
#    app.run(debug=app.config['DEBUG'])