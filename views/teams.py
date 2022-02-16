import json

import flask_praetorian
import sqlalchemy
from flask import request, jsonify, current_app
from flask_restx import abort, Resource, Namespace

import app
from model import Team, db, TeamSchema, Player


# namespace declaration
api_team = Namespace("Teams", "Teams management")

# Controller detailed comments in: users.py

@api_team.route("/<team_id>")
class TeamController(Resource):
    @flask_praetorian.auth_required
    def get(self, team_id):
        team = Team.query.get_or_404(team_id)
        return TeamSchema().dump(team)

    # roles accepted (user with one of these roles)
    @flask_praetorian.roles_accepted("admin", "editor")
    def delete(self, team_id):
        team = Team.query.get_or_404(team_id)
        db.session.delete(team)
        db.session.commit()
        return f"Deleted team {team_id}", 204

    @flask_praetorian.roles_accepted("admin", "editor")
    def put(self, team_id):
        new_team = TeamSchema().load(request.json)
        if str(new_team.id) != team_id:
            abort(400, "id mismatch")
        db.session.commit()
        return TeamSchema().dump(new_team)


@api_team.route("/")
class TeamListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        return TeamSchema(many=True).dump(Team.query.all())

    @flask_praetorian.roles_accepted("admin", "editor")
    def post(self):
        datos = request.json

        if 'imagen' in datos.keys() == True:
            datos["imagen"].save("/static/imagenes/" + datos["imagen"].filename)
            datos["imagen"] = "/static/imagenes/" + datos["imagen"].filename
        else:
            datos["imagen"] = "/static/imagenes/anon.jpg"

        team = TeamSchema().load(datos)
        db.session.add(team)
        db.session.commit()
        return TeamSchema().dump(team), 201

@api_team.route("/subir/<team_id>")
class TeamImageController(Resource):
    @flask_praetorian.auth_required
    def post(self, team_id):
        team = Team.query.get_or_404(team_id)

        imagen = request.files['imagen']
        carpeta = current_app.root_path

        imagen.save(carpeta + "/static/imagenes/" + imagen.filename)

        team.imagen = "/static/imagenes/" + imagen.filename

        db.session.commit()
        return TeamSchema().dump(team)

@api_team.route("/points/<team_id>")
class PlayerController(Resource):
    @flask_praetorian.auth_required
    def get(self, team_id):
        query = sqlalchemy.text('SELECT t.name, SUM(p.puntos) AS puntos FROM team_players tp INNER JOIN player p ON tp.player_id = p.id INNER JOIN team t ON tp.team_id = t.id WHERE tp.team_id = ' + team_id + ' GROUP BY tp.team_id')
        result = db.session.execute(query)
        return jsonify({r['name'] : r['puntos'] for r in result})

@api_team.route("/points/")
class TeamListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        query = sqlalchemy.text('SELECT t.imagen, t.name, SUM(p.puntos) AS puntos FROM team_players tp INNER JOIN player p ON tp.player_id = p.id INNER JOIN team t ON tp.team_id = t.id GROUP BY tp.team_id ORDER BY puntos desc')
        result = db.session.execute(query)
        return jsonify({r['name']:  {'puntos': r['puntos'], "imagen": r["imagen"]} for r in result})
