from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize the database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configure the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sharefare.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the app
    db.init_app(app)

    # Import and register blueprints for the API routes
    from routes import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app

# Create the Flask app instance
app = create_app()

# The app.run() is not required for deployment on Render (uses gunicorn instead)
