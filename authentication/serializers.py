from flask_marshmallow import Marshmallow
from .models import User

ma = Marshmallow()

def init_app(app):
    ma.init_app(app)

class  UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
