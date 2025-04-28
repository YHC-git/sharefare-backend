from flask import Blueprint, request, jsonify
from app import db
from models import User, Ride, Booking
from werkzeug.security import generate_password_hash, check_password_hash

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/api/register', methods=['POST'])
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

@api_blueprint.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful', 'user_id': user.id}), 200

@api_blueprint.route('/api/rides', methods=['POST'])
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

@api_blueprint.route('/api/rides', methods=['GET'])
def get_rides():
    rides = Ride.query.all()
    rides_list = [{
        'id': ride.id,
        'origin': ride.origin,
        'destination': ride.destination,
        'date': ride.date,
        'time': ride.time,
        'available_seats': ride.available_seats
    } for ride in rides]
    return jsonify(rides_list)

@api_blueprint.route('/api/rides/<int:ride_id>/book', methods=['POST'])
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
