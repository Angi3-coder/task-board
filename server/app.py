import os
import bcrypt
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required
)

from models import db, User, Project, Task

app = Flask(__name__)
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI']= os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

#CORS - cross-origin Resourse sharing
CORS(app)

db.init_app(app)
migrate= Migrate(app, db)
jwt=JWTManager(app)

#CORS - IT ALLOWS INENTIONAL COMMUNICATION BETWEEN TRUSTED DOMAIN
#Auth Routes
#signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'All fields required'}), 400
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    user = User(
        username = data['username'],
        email=data['email'],
        password_hash=hashed.decode('utf-8')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'message': 'User created successfully'
    }), 201



if __name__ == '__main__':
    app.run(debug=True, port=8000)