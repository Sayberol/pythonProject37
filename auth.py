import calendar
import datetime

import jwt
from flask import request

from config import Config
from models import User


def generate_token(data):
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)
    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)
    return {'access_token': access_token, 'refresh_token': refresh_token}


def check_token(token):
    try:
        jwt.decode(token, Config.JWT_SECRET, algorithms=Config.JWT_ALGORITHM)
        return True
    except Exception:
        return False


def auth_required(func):
    def wrapper(*args, **kwargs):
        req_json = request.json
        token = req_json.get("access_token")
        if not token:
            return "", 401
        else:
            return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        req_json = request.json
        user_id = req_json.get("user_id")
        user = User.query.get(user_id)
        if user.role == "admin":
            return func(*args, **kwargs)
        else:
            return "", 403
    return wrapper
