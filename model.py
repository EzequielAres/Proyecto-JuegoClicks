from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy_utils import database_exists

# instantiate SQLAlchemy object
db = SQLAlchemy()


def init_db(app, guard, testing=False):
    """
    Initializes database

    :param app: flask app
    :param guard: praetorian object for password hashing if seeding needed
    """
    db.init_app(app)
    if testing or not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        # if there is no database file
        # migrate model
        db.create_all(app=app)
        # seed data
        seed_db(app, guard)


def seed_db(app, guard):
    """
    Seeds database with test data

    :param app: flask app
    :param guard: praetorian object for password hashing
    """
    # when using app var in function, we need to use app_context
    with app.app_context():
        # lists of model objects for db seed
        roles = [
            Role(name="admin"),
            Role(name="editor"),
            Role(name="user")
        ]

        teams = [
            Team(name="Equipo1", imagen="/static/imagenes/anon.jpg"),
            Team(name="Equipo2", imagen="/static/imagenes/anon.jpg"),
            Team(name="Equipo3", imagen="/static/imagenes/anon.jpg"),
            Team(name="Equipo4", imagen="/static/imagenes/anon.jpg"),
            Team(name="Equipo5", imagen="/static/imagenes/anon.jpg")
        ]

        users = [
            User(username="Ezequiel", email="ezequiel@ejemplo.com",
                 hashed_password=guard.hash_password("pestillo"),
                 roles=[roles[0]]),
            User(username="Paco", email="paco@ejemplo.com",
                 hashed_password=guard.hash_password("pestillo"),
                 roles=[roles[2]]),
            User(username="Ana", email="ana@ejemplo.com",
                 hashed_password=guard.hash_password("pestillo"),
                 roles=[roles[0], roles[1]]),
            User(username="María", email="maria@ejemplo.com",
                 hashed_password=guard.hash_password("pestillo"),
                 roles=[roles[2]]),
            User(username="Rocío", email="rocio@ejemplo.com",
                 hashed_password=guard.hash_password("pestillo"),
                 roles=[roles[0]]),
            User(username="Carmen", email="carmen@ejemplo.com",
                 hashed_password=guard.hash_password("pestillo"),
                 roles=[roles[1]]),
            User(username="Rafael", email="rafael@ejemplo.com",
                 hashed_password=guard.hash_password("pestillo"),
                 roles=[roles[2]]),
            User(username="Jose", email="jose@ejemplo.com",
                 hashed_password=guard.hash_password("pestillo"),
                 roles=[roles[2], roles[1]]),
            User(username="Pablo", email="Pablo@ejemplo.com",
                 hashed_password=guard.hash_password("pestillo"),
                 roles=[roles[0]]),
            User(username="Alex", email="alex@ejemplo.com",
                 hashed_password=guard.hash_password("pestillo"),
                 roles=[roles[1]])
        ]

        players = [
            Player(username="Ezequiel", user=users[0], puntos=100, teams=[teams[0], teams[1]], imagen="/static/imagenes/anon.jpg", location_id=1),
            Player(username="Paco", user=users[1], puntos=30, teams=[teams[0]], imagen="/static/imagenes/anon.jpg", location_id=1),
            Player(username="Ana", user=users[2], puntos=55, teams=[teams[1], teams[2]], imagen="/static/imagenes/anon.jpg", location_id=2),
            Player(username="María", user=users[3], puntos=23, teams=[teams[0], teams[1], teams[2]], imagen="/static/imagenes/anon.jpg", location_id=2),
            Player(username="Rocío", user=users[4], puntos=130, teams=[teams[2], teams[1]], imagen="/static/imagenes/anon.jpg", location_id=3),
            Player(username="Carmen", user=users[5], puntos=200, teams=[teams[4], teams[1]], imagen="/static/imagenes/anon.jpg", location_id=4),
            Player(username="Rafael", user=users[6], puntos=123, teams=[teams[4], teams[3]], imagen="/static/imagenes/anon.jpg", location_id=5),
            Player(username="Jose", user=users[7], puntos=76, teams=[teams[3], teams[2]], imagen="/static/imagenes/anon.jpg", location_id=6),
            Player(username="Pablo", user=users[8], puntos=29, teams=[teams[4], teams[0]], imagen="/static/imagenes/anon.jpg", location_id=7),
            Player(username="Alex", user=users[9], puntos=50, teams=[teams[2], teams[3]], imagen="/static/imagenes/anon.jpg", location_id=8)
        ]

        locations = [
            Location(name="Cádiz", region_id=1),
            Location(name="Chiclana", region_id=1),
            Location(name="San Fernando", region_id=1),
            Location(name="Alcorcón", region_id=2),
            Location(name="Horta", region_id=3),
            Location(name="Amares", region_id=4),
            Location(name="Stuttgart", region_id=5),
            Location(name="Flensburgo", region_id=6)
        ]

        regions = [
            Region(name="Andalucía", country_id=1),
            Region(name="Madrid", country_id=1),
            Region(name="Açores", country_id=2),
            Region(name="Braga", country_id=2),
            Region(name="Baden-Wurtemberg", country_id=3),
            Region(name="Schleswig-Holstein", country_id=3)
        ]

        countries= [
            Country(name="España"),
            Country(name="Portugal"),
            Country(name="Alemania"),
        ]

        # add data from lists
        for user in users:
            db.session.add(user)
        for player in players:
            db.session.add(player)
        for team in teams:
            db.session.add(team)
        for location in locations:
            db.session.add(location)
        for region in regions:
            db.session.add(region)
        for country in countries:
            db.session.add(country)
        # commit changes in database
        db.session.commit()


# table for N:M relationship
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
                       )


# classes for model entities
class User(db.Model):
    """
    User entity

    Store user data
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # se puede declarar la relación en ambos lados usando backref
    # si se usara back_populates es necesario declararla en ambos lados
    # user = db.relationship("Owner", backref=db.backref("user", uselist=False))

    # from praetorian example
    hashed_password = db.Column(db.Text)
    # M:N relationship
    roles = db.relationship('Role', secondary=roles_users)
    is_active = db.Column(db.Boolean, default=True, server_default="true")

    # this enable this entity as user entity in praetorian
    @property
    def identity(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has an ``identity`` instance
        attribute or property that provides the unique id of the user instance
        """
        return self.id

    @property
    def rolenames(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has a ``rolenames`` instance
        attribute or property that provides a list of strings that describe the roles
        attached to the user instance
        """
        # try:
        #     return self.roles.split(",")
        # except Exception:
        #     return []
        return [role.name for role in self.roles]

    @property
    def password(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has a ``password`` instance
        attribute or property that provides the hashed password assigned to the user
        instance
        """

        return self.hashed_password

    @classmethod
    def lookup(cls, username):
        """
        *Required Method*

        flask-praetorian requires that the user class implements a ``lookup()``
        class method that takes a single ``username`` argument and returns a user
        instance if there is one that matches or ``None`` if there is not.
        """
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id_user):
        """
        *Required Method*

        flask-praetorian requires that the user class implements an ``identify()``
        class method that takes a single ``id`` argument and returns user instance if
        there is one that matches or ``None`` if there is not.
        """
        return cls.query.get(id_user)

    def is_valid(self):
        return self.is_active

    # specify string for repr
    def __repr__(self):
        return f"<User {self.username}>"


class Role(db.Model):
    """
    Role entity

    Store roles data
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f"<Role {self.name}>"


team_players = db.Table('team_players',
                        db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True),
                        db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
                        )


class Player(db.Model):
    """
    Player entity

    Store player data
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    puntos = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.String(150), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref=db.backref("player", uselist=False))

    teams = db.relationship('Team', secondary=team_players)
    is_active = db.Column(db.Boolean, default=True, server_default="true")

    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship("Location", backref="Player")

    def __repr__(self):
        return f"<User {self.username}>"


class Team(db.Model):
    """
     Team entity

     Store team data
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    imagen = db.Column(db.String(150), unique=False, nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"

class Location(db.Model):
    """
    Location entity

    Store location data
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    region = db.relationship("Region", backref="Location")

    def __repr__(self):
        return f"<User {self.name}>"


class Region(db.Model):
    """
    Region entity

    Store region data
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country = db.relationship("Country", backref="Region")

    def __repr__(self):
        return f"<User {self.name}>"


class Country(db.Model):
    """
    Country entity

    Store country data
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"


# Marshmallow schemas definition
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        # model class for the schema
        model = User
        include_relationships = True
        load_instance = True
        sqla_session = db.session


class PlayerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Player
        include_relationships = True
        load_instance = True
        sqla_session = db.session


class LocationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        include_relationships = True
        load_instance = True
        sqla_session = db.session


class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        include_relationships = True
        load_instance = True
        sqla_session = db.session

class TeamSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        include_relationships = True
        load_instance = True
        sqla_session = db.session

class RegionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Region
        include_relationships = True
        load_instance = True
        sqla_session = db.session

class CountrySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Country
        include_relationships = True
        load_instance = True
        sqla_session = db.session