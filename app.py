from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sharefare.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database
    db.init_app(app)

    # Import and register blueprints
    from routes import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app

# Create the app instance
app = create_app()

# No need to call app.run() here; Render uses gunicorn to serve the app
