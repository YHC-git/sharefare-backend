from flask import Blueprint, request, jsonify
from app import db
from models import User, Ride, Booking
from werkzeug.security import generate_password_hash, check_password_hash

api_blueprint = Blueprint('api', __name__)

# User Registration
@api_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing fields'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# User Login
@api_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful', 'user_id': user.id}), 200

# Create a Ride
@api_blueprint.route('/rides', methods=['POST'])
def create_ride():
    data = request.get_json()
    new_ride = Ride(
        driver_id=data['driver_id'],
        origin=data['origin'],
        destination=data['destination'],
        date=data['date'],
        time=data['time'],
        available_seats=data['available_seats']
    )
    db.session.add(new_ride)
    db.session.commit()

    return jsonify({'message': 'Ride created successfully'}), 201

# Get All Rides (with optional search)
@api_blueprint.route('/rides', methods=['GET'])
def get_rides():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    date = request.args.get('date')

    query = Ride.query

    if origin:
        query = query.filter(Ride.origin.ilike(f'%{origin}%'))
    if destination:
        query = query.filter(Ride.destination.ilike(f'%{destination}%'))
    if date:
        query = query.filter(Ride.date == date)

    rides = query.all()

    rides_list = [{
        'id': ride.id,
        'driver_id': ride.driver_id,
        'origin': ride.origin,
        'destination': ride.destination,
        'date': ride.date,
        'time': ride.time,
        'available_seats': ride.available_seats
    } for ride in rides]

    return jsonify(rides_list)

# Book a Ride
@api_blueprint.route('/rides/<int:ride_id>/book', methods=['POST'])
def book_ride(ride_id):
    data = request.get_json()
    user_id = data.get('user_id')
    seats_booked = data.get('seats_booked')

    ride = Ride.query.get_or_404(ride_id)

    if ride.available_seats < seats_booked:
        return jsonify({'error': 'Not enough seats available'}), 400

    ride.available_seats -= seats_booked

    booking = Booking(ride_id=ride_id, user_id=user_id, seats_booked=seats_booked)
    db.session.add(booking)
    db.session.commit()

    return jsonify({'message': 'Ride booked successfully'}), 200

# Get All Users (for browse users feature)
@api_blueprint.route('/users', methods=['GET'])
def browse_users():
    users = User.query.all()
    users_list = [{
        'id': user.id,
        'email': user.email
    } for user in users]

    return jsonify(users_list)
