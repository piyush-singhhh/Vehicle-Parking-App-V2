#  step for create Virtual Environment for the project
# python -m venv venv 
# activate the virtual environment
# source venv/bin/activate


# 1. Go to your project folder
# cd ~/path/to/your/project

# 2. Initialize Git (only once)
# git init

# 3. Add remote GitHub repo
# git remote add origin https://github.com/USERNAME/REPO_NAME.git

# 4. Stage all files
# git add .

# 5. Commit files with a message
# git commit -m "Initial commit: Flask Parking App"

# 6. Set branch to main (optional)
# git branch -M main

# 7. Push code to GitHub
# git push -u origin main

# 8. For future changes:
# git add .
# git commit -m "Your message"
# git push
import os
from flask import Flask
from applications.models import db, User, Role, Parking_lot, ParkingSpot, History
from applications.config import LocalDevelopmentConfig
from flask_security import SQLAlchemyUserDatastore, datastore , Security
from flask_security.utils import hash_password



def create_app():
    # Create Flask app
    app = Flask(__name__, instance_relative_config=True)

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Load configuration
    app.config.from_object(LocalDevelopmentConfig)

    # Dynamically set SQLite URI using instance_path
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'parking.db')

    # Initialize database
    db.init_app(app)

    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)


    # Create all tables if they don't exist
    with app.app_context():
        db.create_all()

    # Define routes
    @app.route('/')
    def home():
        return "Flask Parking App is running with one DB file in instance/"
    return app

def create_roles_and_admin():
    roles = ["admin", "user"]
    for role in roles:
        app.security.datastore.find_or_create_role(name=role)
    db.session.commit()
    if not app.security.datastore.find_user(email="admin@gmail.com"):
        app.security.datastore.create_user(
            email="admin@gmail.com",
            password=hash_password('6299087198'),
            name="Admin",
            roles=["admin"] 
        )
    db.session.commit() 

def add_user():
    if not app.security.datastore.find_user(email="user1@gmail.com"):
        app.security.datastore.create_user(
            email="user1@gmail.com",
            password=hash_password("6299087198"),
            name="User1",
            roles= ["user"]
            )
    db.session.commit()

# Run the app
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # create_roles_and_admin()
        add_user()
    app.run()
