from datetime import datetime

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
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)

    @property
    def local(self):
        return {
            'city': self.city,
            'state': self.state,
        }

    @property
    def past_shows(self):
        shows = Show.query.filter(
            Show.start_time < datetime.now(),
            Show.venue_id == self.id).all()
        return [{
            'artist_id': show.artist.id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for show in shows]

    @property
    def past_shows_count(self):
        return len(self.past_shows)

    @property
    def upcoming_shows(self):
        shows = Show.query.filter(
            Show.start_time > datetime.now(),
            Show.venue_id == self.id).all()
        return [{
            'artist_id': show.artist.id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for show in shows]

    @property
    def upcoming_shows_count(self):
        return len(self.upcoming_shows)


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
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)

    @property
    def past_shows(self):
        shows = Show.query.filter(
            Show.start_time < datetime.now(),
            Show.artist_id == self.id).all()
        return [{
            'venue_id': show.venue.id,
            'venue_name': show.venue.name,
            'venue_image_link': show.venue.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for show in shows]

    @property
    def past_shows_count(self):
        return len(self.past_shows)

    @property
    def upcoming_shows(self):
        shows = Show.query.filter(
            Show.start_time > datetime.now(),
            Show.artist_id == self.id).all()
        return [{
            'venue_id': show.venue.id,
            'venue_name': show.venue.name,
            'venue_image_link': show.venue.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for show in shows]

    @property
    def upcoming_shows_count(self):
        return len(self.upcoming_shows)


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

    @property
    def complete(self):
        return {
            "venue_id": self.venue_id,
            "venue_name": self.venue.name,
            "artist_id": self.artist_id,
            "artist_name": self.artist.name,
            "artist_image_link": self.artist.image_link,
            "start_time": self.start_time.strftime("%m/%d/%Y, %H:%M")
        }
