from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.config_app.Config')

    CORS(app, resources={
        r'/api/': {
            'origins': '*'
        }
    })
    return app

