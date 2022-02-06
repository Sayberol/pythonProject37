import calendar
import datetime

import jwt
from flask import request
from flask_restx import Namespace, Resource
from sqlalchemy.orm import session

from auth import generate_token, check_token
from models import User
from setup_db import db

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        json_user_name = req_json.get("username")
        user_pass = req_json.get("password")
        user = db.session.query(User).filter_by(username=json_user_name).first()
        if user and user.password == user_pass:
            response = generate_token(req_json)
            return response, 200
        else:
            return "", 401

    def put(self):
        req_json = request.json
        refresh_token = req_json.get("refresh_token")
        if check_token(refresh_token):
            response = generate_token(req_json)
            return response, 200
        else:
            return "", 401
