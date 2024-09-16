from flask import Flask
from app.game import tic_tac_toe_bp
from app.utils import get_redis_connection
from .config import Config
from flask_cors import CORS

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    # Initilize redis connection
    app.redis = get_redis_connection(app.config)

    # register blueprints
    app.register_blueprint(tic_tac_toe_bp)

    return app
