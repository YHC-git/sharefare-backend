from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Database config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sharefare.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Optional root route
    @app.route('/')
    def index():
        return 'Welcome to ShareFare Backend API! Use /api endpoints.'

    # Register API blueprint
    from routes import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app

# Create the Flask app instance
app = create_app()
