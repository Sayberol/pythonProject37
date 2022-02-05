import calendar
import datetime

import jwt
from flask import request
from flask_restx import Namespace, Resource

from lesson19_project_easy_source.auth import generate_token, check_token
from lesson19_project_easy_source.models import User

auth_ns = Namespace('auth')


@auth_ns.route(Resource)
class AuthView('/'):
    def post(self):
        req_json = request.json
        user_name = req_json.get("username")
        user_pass = req_json.get("password")
        user = User.get_filter({"username": user_name})
        if not user and user.password == user_pass:
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
