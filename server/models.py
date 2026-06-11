from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) #constraint
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    projects = db.relationship('Project', back_populates='user', cascade='all, delete-orphan')


#Project model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', back_populates='projects')
    tasks = db.relationship('Task', back_populates='project', cascade = 'all, delete-orphan')


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='todo')
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    project = db.relationship('Project', back_populates='tasks')