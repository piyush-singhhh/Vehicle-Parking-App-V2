from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

# Bridge table for many-to-many relation
user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'), primary_key=True)
)

# User table
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True)
    name = db.Column(db.String(30), nullable=False)

    # Many-to-many with roles
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', passive_deletes=True))

# Role table
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

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

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    vehicle_number = db.Column(db.String(20), nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)

    lot = db.relationship('Parking_lot', back_populates='spots')
    user = db.relationship('User', backref='occupied_spots')

    # def calculate_duration_hours(self):
    #     if self.start_time and self.end_time:
    #         delta = self.end_time - self.start_time
    #         return round(delta.total_seconds() / 3600, 2)
    #     return 0

    # def calculate_cost(self):
    #     duration = self.calculate_duration_hours()
    #     if duration and self.lot:
    #         return round(duration * self.lot.price_per_hour, 2)
    #     return 0


class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    
    vehicle_number = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    total_time = db.Column(db.String(50), nullable=True)
    total_price = db.Column(db.Float, nullable=True)
