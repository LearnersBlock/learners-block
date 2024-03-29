import bcrypt
import config
from common.errors import logger
from common.processes import database_recover
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import expression

db = SQLAlchemy()
migrate = Migrate()
salt = bcrypt.gensalt()
default_password = (
    b"$2b$09$PBTwpPOtvyN6KQG6C9VPgutig3jX.1VVyqxIveoBfzMD/msTYNf0e"
)


# Create default user
def init_database():
    try:
        db.create_all()
        if not User.query.filter_by(username=config.default_hostname).first():
            lb_database = User(password=default_password)
            db.session.add(lb_database)
            db.session.commit()
    except Exception:
        logger.exception("Database error during initialisation.")
        database_recover()


# Set App Store database content
class App_Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    author_site = db.Column(db.String, unique=False, nullable=True)

    dependencies = db.Column(db.String, unique=False, nullable=True)

    env_vars = db.Column(db.String, unique=False, nullable=True)

    image = db.Column(db.String, unique=False, nullable=False)

    info = db.Column(db.String, unique=False, nullable=False)

    logo = db.Column(db.String, unique=False, nullable=True)

    long_name = db.Column(db.Text, unique=False, nullable=False)

    ports = db.Column(db.Integer, unique=False, nullable=False)

    version = db.Column(db.Integer, unique=False, nullable=False)

    version_name = db.Column(db.Text, unique=False, nullable=False)

    status = db.Column(
        db.String, unique=False, server_default="install", nullable=False
    )

    volumes = db.Column(db.String, unique=False, nullable=True)

    def __repr__(self):
        return "<App_Store %r>" % self.name

    def commit():
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


# Set user database content
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String,
        unique=True,
        server_default=config.default_hostname,
        nullable=False,
    )

    password = db.Column(
        db.String,
        unique=False,
        server_default=str(default_password),
        nullable=False,
    )

    allow_password_reset = db.Column(
        db.Boolean,
        unique=False,
        server_default=expression.true(),
        nullable=False,
    )

    files = db.Column(
        db.Boolean,
        unique=False,
        server_default=expression.true(),
        nullable=False,
    )

    library = db.Column(
        db.Boolean,
        unique=False,
        server_default=expression.true(),
        nullable=False,
    )

    website = db.Column(
        db.Boolean,
        unique=False,
        server_default=expression.true(),
        nullable=False,
    )

    start_page = db.Column(
        db.String, unique=False, server_default=str("/"), nullable=False
    )

    wifi_password = db.Column(
        db.String, unique=False, server_default=str(""), nullable=True
    )

    wifi_ssid = db.Column(
        db.String, server_default=str(config.default_ssid), unique=False
    )

    def __repr__(self):
        return "<User %r>" % self.username

    def hash_password(password):
        return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt(9))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def verify_password(password, hashed_password):
        return bcrypt.checkpw(password.encode("utf8"), hashed_password)
