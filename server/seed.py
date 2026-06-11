import bcrypt
from faker import Faker
from app import app
from models import db, User, Project, Task

fake = Faker()

with app.app_context():
    #clear existing data
    Task.query.delete()
    Project.query.delete()
    User.query.delete()

    users= []

    for i in range (10):
        password = "password123"

        user = User(
            username=fake.user_name(),
            email = fake.unique.email(),
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()). decode('utf-8')
        )
        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    print('Users seeded successfully')

    #projects
    projects= []

    for user in users:
        for i in range(2):
            project = Project(
                name = fake.catch_phrase(),
                description=fake.text(max_nb_chars=100),
                user_id = user.id
            )
            projects.append(project)
    
    db.session.add_all(projects)
    db.session.commit()

    print('Projects seeded successfully')

    #create Tasks

    statuses = ['todo', 'in_progress', 'done']

    tasks = []
    for project in projects:
        for i in range (2):
            task = Task(
                title= fake.sentence(nb_words=4),
                status= fake.random_element(statuses),
                project_id = project.id
            )
            tasks.append(task)
    db.session.add_all(tasks)
    db.session.commit()

    print('tasks seeded successfully')