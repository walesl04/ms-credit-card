from flask import Blueprint, make_response, abort, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
from functools import wraps
from datetime import datetime, timedelta
from .models import User
from .serializers import UserSchema
from utils.enums import  HTTPCode

bp_user = Blueprint('user', __name__)
user_sc = UserSchema(many=True)

def token_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token: 
            return make_response({
                'message': 'missing token!'
            }, HTTPCode.FORBIDDEN.value)
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(uuid=data['uuid']).first()
        except Exception as e:
            print('log:e', e)
            return make_response({ 'message': 'Token is invalid!' }, HTTPCode.NOT_AUTHORIZATION.value)
        
        return function(current_user, *args, **kwargs)

    return decorated


@bp_user.get('/user')
@token_required
def index(current_user):
    try:
        all_users = User.query.all()
        return make_response(user_sc.dump(all_users), HTTPCode.SUCCESS.value)
    except Exception as e:
        abort(HTTPCode.BAD_REQUEST.value)

@bp_user.post('/user')
def create():
    try:
        data = request.get_json()
        if data.get('password') is None or data.get('email') is None:
            raise Exception('Required fields!')

        hashed_password = generate_password_hash(data.get('password'), method='sha256')
        uuid_user = uuid.uuid4()
        data['uuid'] = str(uuid_user)
        data['password'] = hashed_password
        user_sc = UserSchema()
        print('log:data', data)
        user = user_sc.load(data)

        current_app.db.session.add(user)
        current_app.db.session.commit()

        return make_response(user_sc.jsonify(user), HTTPCode.CREATED.value)
    except Exception as e:
        abort(HTTPCode.BAD_REQUEST.value)


@bp_user.get('/user/<int:id_user>')
def find_user(id_user):
    try:
        user = User.query.get_or_404(id_user)

        user_sc = UserSchema()

        return make_response(user_sc.jsonify(user), HTTPCode.SUCCESS.value)
    except Exception as e:
        abort(HTTPCode.BAD_REQUEST.value)

@bp_user.post('/login')
def login():
    auth = request.get_json()

    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response('Not Authorization 1', HTTPCode.NOT_AUTHORIZATION.value, {
            'WWW-Authenticate': 'Basic realm="Login required!"'
        })
    
    user = User.query.filter_by(email=auth.get('email')).first()
    print('Log:user', user, auth.get('email'))
    if not user:
        return make_response('Not Authorization 2', HTTPCode.NOT_AUTHORIZATION.value, {
            'WWW-Authenticate': 'Basic realm="Login required!"'
        })

    if check_password_hash(user.password, auth.get('password')):
        token = jwt.encode({
            'uuid': user.uuid,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, current_app.config['SECRET_KEY'])
        return make_response({
            'token': token
        })
    
    return make_response('Not Authorization 3', HTTPCode.NOT_AUTHORIZATION.value, {
            'WWW-Authenticate': 'Basic realm="Login required!"'
        })

