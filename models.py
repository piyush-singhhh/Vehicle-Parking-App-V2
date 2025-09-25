from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()  # define db here so it can be imported in app.py


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    pin_code = db.Column(db.String(6), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class Parking_lot(db.Model):
    __tablename__ = 'parking_lot'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parking_lot_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    pin_code = db.Column(db.String(6), nullable=False)
    price_per_hour = db.Column(db.Integer, nullable=False)
    total_capacity = db.Column(db.Integer, nullable=False)
    avilable_capacity = db.Column(db.Integer, nullable=False)
    spots = db.relationship("ParkingSpot", back_populates='lot')


class ParkingSpot(db.Model):
    __tablename__ = 'parking_spot'
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    spot_number = db.Column(db.String(10), nullable=False)
    is_occupied = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    vehicle_number = db.Column(db.String(20), nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)

    lot = db.relationship('Parking_lot', back_populates='spots')
    user = db.relationship('User', backref='occupied_spots')

    def calculate_duration_hours(self):
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            return round(delta.total_seconds() / 3600, 2)
        return 0

    def calculate_cost(self):
        duration = self.calculate_duration_hours()
        if duration and self.lot:
            return round(duration * self.lot.price_per_hour, 2)
        return 0


class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    
    vehicle_number = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    total_time = db.Column(db.String(50), nullable=True)
    total_price = db.Column(db.Float, nullable=True)
