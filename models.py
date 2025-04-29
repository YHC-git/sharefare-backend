from app import db

# -------------------
# User Model
# -------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    tel_num = db.Column(db.String(15))
    gender = db.Column(db.String(10))
    dob = db.Column(db.String(20))
    avatar = db.Column(db.String(255))  # URL or path to image

    # Relationships
    rides = db.relationship('Ride', backref='driver', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)

# -------------------
# Ride Model
# -------------------
class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    origin = db.Column(db.String(120), nullable=False)
    destination = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)

    # Relationships
    bookings = db.relationship('Booking', backref='ride', lazy=True)

# -------------------
# Booking Model
# -------------------
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ride_id = db.Column(db.Integer, db.ForeignKey('ride.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seats_booked = db.Column(db.Integer, nullable=False)
