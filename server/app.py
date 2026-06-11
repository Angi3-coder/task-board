import os
import bcrypt
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
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

#log in
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()

    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({'error': 'Invalid Credetials'}), 401
    
    token = create_access_token(identity=str(user.id))

    return jsonify({'token': token, 'username': user.username}), 200


#profile
@app.route('/me', methods=[ 'GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    projects= []

    for project in user.projects:
        project_dict = {
            'id': project.id,
            'name': project.name, 
            'description': project.description,
            "tasks": [
                {
                    'id': task.id,
                    'title': task.title,
                    'status': task.status
                } for task in project.tasks
            ]
        }
        projects.append(project_dict)

    return jsonify ({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'projects': projects
    }), 200






if __name__ == '__main__':
    app.run(debug=True, port=8000)