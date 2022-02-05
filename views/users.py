

from flask import request
from flask_restx import Namespace, Resource

from models import User, UserSchema
from setup_db import db

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        rs = db.session.query(User).all()
        res = UserSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        req_json = request.json
        ent = User(**req_json)

        db.session.add(ent)
        db.session.commit()
        return "", 201


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def put(self, uid):
        user = User.query.get(uid)
        if not user:
            db.session.add(user)
            db.session.commit()
            return "", 201
        else:
            db.session.update(user)
            db.session.commit()
            return "", 200

