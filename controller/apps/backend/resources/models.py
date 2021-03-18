from sqlalchemy.sql import expression
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import bcrypt

db = SQLAlchemy()
migrate = Migrate()
salt = bcrypt.gensalt()
default_password = \
    b'$2b$12$x70yiBuLG/YQ3GOyGlFdAOBB/NaJUFQulqSOH4WrznxZVnAmWVl9S'


# Create default user
def create_default_user():
    if not User.query.filter_by(username='lb').first():
        lb_database = User(password=default_password)
        db.session.add(lb_database)
        db.session.commit()


# Set database content
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True,
                         server_default='lb',
                         nullable=False)

    password = db.Column(db.String(128), unique=False,
                         server_default=str(default_password),
                         nullable=False)

    files = db.Column(db.Boolean, unique=False,
                      server_default=expression.true(),
                      nullable=False)

    library = db.Column(db.Boolean, unique=False,
                        server_default=expression.true(),
                        nullable=False)

    makerspace = db.Column(db.Boolean, unique=False,
                           server_default=expression.true(),
                           nullable=False)

    website = db.Column(db.Boolean, unique=False,
                        server_default=expression.true(),
                        nullable=False)

    allow_password_reset = db.Column(db.Boolean, unique=False,
                                     server_default=expression.true(),
                                     nullable=False)

    start_page = db.Column(db.String(80), unique=False,
                           server_default=str("menu"),
                           nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(12))

    def verify_password(password, hashed_password):
        return bcrypt.checkpw(password.encode('utf8'), hashed_password)
