from flask import request
from flask_restx import Resource, Namespace



from auth import auth_required, admin_required
from models import Director, DirectorSchema
from setup_db import db

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = db.session.query(Director).all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        add_movie = Director(**req_json)
        with db.session.begin():
            db.session.add(add_movie)
        return "", 201


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @auth_required
    def get(self, rid):
        r = db.session.query(Director).get(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, rid):
        director = Director.query.get(rid)
        if not director:
            db.session.add(director)
            db.session.commit()
            return "", 201
        else:
            db.session.update(director)
            db.session.commit()
            return "", 204

    @admin_required
    def delete(self, rid):
        director = Director.query.get(rid)
        if not director:
            return "", 404
        else:
            db.session.delete(director)
            db.session.commit()
            return "", 204
