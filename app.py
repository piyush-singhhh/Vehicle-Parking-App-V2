#  step for create Virtual Environment for the project
# python -m venv venv 
# activate the virtual environment
# source venv/bin/activate
from flask import Flask, render_template, request, redirect ,url_for, flash
from datetime import datetime ,timedelta
from flask import Response
from flask_migrate import Migrate
import os
from models import db, User, Parking_lot, ParkingSpot, History

app = Flask(__name__, instance_relative_config=True)

# Configurations
app.secret_key = "123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'parking.db')
# Disable SQLAlchemy event system to save memory and improve performance.
# If not set, Flask will show a warning and use extra resources unnecessarily.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

# Initialize database
db.init_app(app)

with app.app_context():
    db.create_all()

# Example route
@app.route('/')
def home():
    return "🚗 Flask Parking App - Version 2 is running with DB inside instance/!"

if __name__ == "__main__":
    app.run(debug=True)
