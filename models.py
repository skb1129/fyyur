from flask_sqlalchemy import SQLAlchemy

import config

database_name = 'trivia'
database_path = f'postgresql://localhost:5432/{database_name}'

db = SQLAlchemy()


def setup_db(app):
    app.config.from_object(config)
    db.app = app
    db.init_app(app)
    db.create_all()


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    @property
    def local(self):
        return {
            'city': self.city,
            'state': self.state,
        }


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime())
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'),
                          nullable=False)
    artist = db.relationship('Artist',
                             backref=db.backref('shows', cascade="all,delete"))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    venue = db.relationship('Venue',
                            backref=db.backref('shows', cascade="all,delete"))
