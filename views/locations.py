import json

import flask_praetorian
import sqlalchemy
from flask import request, jsonify
from flask_restx import abort, Resource, Namespace

from model import Location, db, LocationSchema

# namespace declaration
api_location = Namespace("Locations", "Locations management")

# Controller detailed comments in: users.py

@api_location.route("/<location_id>")
class LocationController(Resource):
    @flask_praetorian.auth_required
    def get(self, location_id):
        location = Location.query.get_or_404(location_id)
        return LocationSchema().dump(location)

    # roles accepted (user with one of these roles)
    @flask_praetorian.roles_accepted("admin", "editor")
    def delete(self, location_id):
        location = Location.query.get_or_404(location_id)
        db.session.delete(location)
        db.session.commit()
        return f"Deleted location {location_id}", 204

    @flask_praetorian.roles_accepted("admin", "editor")
    def put(self, location_id):
        new_location = LocationSchema().load(request.json)
        if str(new_location.id) != location_id:
            abort(400, "id mismatch")
        db.session.commit()
        return LocationSchema().dump(new_location)


@api_location.route("/")
class LocationListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        return LocationSchema(many=True).dump(Location.query.all())

    @flask_praetorian.roles_accepted("admin", "editor")
    def post(self):
        location = LocationSchema().load(request.json)
        db.session.add(location)
        db.session.commit()
        return LocationSchema().dump(location), 201

# TODO: Dump query to json
@api_location.route("/points/<location_id>")
class LocationController(Resource):
    @flask_praetorian.auth_required
    def get(self, location_id):
        query = sqlalchemy.text('SELECT l.name, SUM(p.puntos) AS puntos FROM player p INNER JOIN location l ON l.id = p.location_id WHERE l.id =' + location_id + ' GROUP BY l.name')
        result = db.session.execute(query)
        return jsonify({r['name'] : r['puntos'] for r in result})

@api_location.route("/points/")
class LocationListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        query = sqlalchemy.text('SELECT l.name, SUM(p.puntos) AS puntos FROM player p INNER JOIN location l ON l.id = p.location_id GROUP BY l.name ORDER BY puntos desc')
        result = db.session.execute(query)
        return jsonify({r['name'] : r['puntos'] for r in result})

