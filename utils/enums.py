from enum import Enum

class HTTPCode(Enum):
    SUCCESS = 200
    CREATED = 201
    BAD_REQUEST = 400
    FORBIDDEN = 403
    NOT_FOUND = 404
    NOT_AUTHORIZATION = 401
