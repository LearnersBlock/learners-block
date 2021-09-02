from common.system_processes import database_recover
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from resources.errors import print_message
from sqlalchemy.sql import expression
import bcrypt

db = SQLAlchemy()
migrate = Migrate()
salt = bcrypt.gensalt()
default_password = \
    b'$2b$12$x70yiBuLG/YQ3GOyGlFdAOBB/NaJUFQulqSOH4WrznxZVnAmWVl9S'


# Create default user
def init_database():
    try:
        db.create_all()
        if not User.query.filter_by(username='lb').first():
            lb_database = User(password=default_password)
            db.session.add(lb_database)
            db.session.commit()
    except Exception as ex:
        print_message('init_database',
                      'Database error. '
                      'Trying to recover.',
                      ex)
        database_recover()


# Set App Store database content
class App_Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,
                     unique=True,
                     nullable=False)

    long_name = db.Column(db.String,
                          unique=False,
                          nullable=False)

    env_vars = db.Column(db.String,
                         unique=False,
                         nullable=True)

    image = db.Column(db.String,
                      unique=False,
                      nullable=False)

    ports = db.Column(db.Integer,
                      unique=False,
                      nullable=False)

    volumes = db.Column(db.String,
                        unique=False,
                        nullable=True)

    dependencies = db.Column(db.String,
                             unique=False,
                             nullable=True)

    version = db.Column(db.Text,
                        unique=False,
                        nullable=False)

    author_site = db.Column(db.String,
                            unique=False,
                            nullable=True)

    logo = db.Column(db.String,
                     unique=False,
                     nullable=True)

    status = db.Column(db.String,
                       unique=False,
                       server_default='install',
                       nullable=False)

    def __repr__(self):
        return '<App_Store %r>' % self.name

    def commit():
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


# Set user database content
class User(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String,
                         unique=True,
                         server_default='lb',
                         nullable=False)

    password = db.Column(db.String,
                         unique=False,
                         server_default=str(default_password),
                         nullable=False)

    files = db.Column(db.Boolean,
                      unique=False,
                      server_default=expression.true(),
                      nullable=False)

    library = db.Column(db.Boolean,
                        unique=False,
                        server_default=expression.true(),
                        nullable=False)

    website = db.Column(db.Boolean,
                        unique=False,
                        server_default=expression.true(),
                        nullable=False)

    allow_password_reset = db.Column(db.Boolean,
                                     unique=False,
                                     server_default=expression.true(),
                                     nullable=False)

    start_page = db.Column(db.String,
                           unique=False,
                           server_default=str('/'),
                           nullable=False)

    wifi_password = db.Column(db.String,
                              unique=False,
                              nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(12))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def verify_password(password, hashed_password):
        return bcrypt.checkpw(password.encode('utf8'), hashed_password)