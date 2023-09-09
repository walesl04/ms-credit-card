from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from authentication import models as UserModels, serializers as UserSerializers
from authentication.app import bp_user

def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config.from_object('config.config_app.Config')
    UserModels.init_app(app)
    UserSerializers.init_app(app)

    migrate = Migrate(app, app.db)
    

    CORS(app, resources={
        r'/api/': {
            'origins': '*'
        }
    })

    app.register_blueprint(bp_user)
    return app

