import json

import flask_praetorian
import sqlalchemy
from flask import request, jsonify
from flask_restx import abort, Resource, Namespace

from model import Country, db, CountrySchema

# namespace declaration
api_country = Namespace("Countries", "Countries management")

# Controller detailed comments in: users.py

@api_country.route("/<country_id>")
class CountryController(Resource):
    @flask_praetorian.auth_required
    def get(self, country_id):
        country = Country.query.get_or_404(country_id)
        return CountrySchema().dump(country)

    # roles accepted (user with one of these roles)
    @flask_praetorian.roles_accepted("admin", "editor")
    def delete(self, country_id):
        country = Country.query.get_or_404(country_id)
        db.session.delete(country)
        db.session.commit()
        return f"Deleted country {country_id}", 204

    @flask_praetorian.roles_accepted("admin", "editor")
    def put(self, country_id):
        new_country = CountrySchema().load(request.json)
        if str(new_country.id) != country_id:
            abort(400, "id mismatch")
        db.session.commit()
        return CountrySchema().dump(new_country)


@api_country.route("/")
class CountryListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        return CountrySchema(many=True).dump(Country.query.all())

    @flask_praetorian.roles_accepted("admin", "editor")
    def post(self):
        country = CountrySchema().load(request.json)
        db.session.add(country)
        db.session.commit()
        return CountrySchema().dump(country), 201

# TODO: Dump query to json
@api_country.route("/points/<country_id>")
class CountryController(Resource):
    @flask_praetorian.auth_required
    def get(self, country_id):
        query = sqlalchemy.text('SELECT c.name, SUM(p.puntos) AS puntos FROM player p INNER JOIN location l ON l.id = p.location_id INNER JOIN region r ON r.id = l.region_id INNER JOIN country c on r.country_id = c.id WHERE r.id = ' + country_id + ' GROUP BY c.name')
        result = db.session.execute(query)
        return jsonify({r['name'] : r['puntos'] for r in result})

@api_country.route("/points/")
class CountryListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        query = sqlalchemy.text('SELECT c.name, SUM(p.puntos) AS puntos FROM player p INNER JOIN location l ON l.id = p.location_id INNER JOIN region r ON r.id = l.region_id INNER JOIN country c on r.country_id = c.id GROUP BY c.name ORDER BY SUM(p.puntos) desc')
        result = db.session.execute(query)
        return jsonify({r['name'] : r['puntos'] for r in result})