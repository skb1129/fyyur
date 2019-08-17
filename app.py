# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import logging
from logging import FileHandler, Formatter

import babel
import dateutil.parser
from flask import flash, Flask, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_moment import Moment

from forms import *
from models import Artist, db, setup_db, Show, Venue

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
setup_db(app)
moment = Moment(app)
migrate = Migrate(app, db)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    """
    Render home page
    :return: Home page
    """
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    """
    Render venues list page
    :return: Venues list page
    """
    data = [venue.local for venue in
            Venue.query.distinct(Venue.city, Venue.state).all()]
    for location in data:
        location["venues"] = Venue.query.filter_by(
            city=location["city"],
            state=location["state"])
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    """
    Render venues based on the search term
    :return: Searched venues page
    """
    search = request.form.get('search_term', '')
    data = Venue.query.filter(Venue.name.ilike("%" + search + "%")).all()
    response = {
        "count": len(data),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    """
    Render venue page based on venue id
    :param venue_id: Id of the venue to be displayed
    :return: Venue page
    """
    venue = Venue.query.filter_by(id=venue_id).first_or_404()
    return render_template('pages/show_venue.html', venue=venue)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    """
    Render form to create venue
    :return: New venue form page
    """
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    """
    Create a new venue in database
    :return: Home page
    """
    form = VenueForm(request.form)

    try:
        new_venue = Venue(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            address=form.address.data,
            phone=form.phone.data,
            genres=form.genres.data,
            image_link=form.image_link.data,
            facebook_link=form.facebook_link.data,
            seeking_talent=form.seeking_talent.data,
            seeking_description=form.seeking_description.data
        )
        db.session.add(new_venue)
        db.session.commit()
        flash(f"Venue {form.name.data} was successfully listed!")
    except Exception:
        flash(
            f"An error occurred. Venue {form.name.data} could not be listed.")

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    """
    Delete venue from database
    :param venue_id: Id of venue to be deleted
    :return: None
    """
    try:
        venue = Venue.query.filter_by(id=venue_id).first_or_404()
        db.session.delete(venue)
        db.session.commit()
        flash(f'Venue has been removed.')
        return render_template('pages/home.html')
    except ValueError:
        flash('Error while deleting the venue.')

    return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    """
    Render artists list page
    :return: Artists list page
    """
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    """
    Render artists based on the search term
    :return: Searched artists page
    """
    search = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike("%" + search + "%")).all()
    response = {
        "count": len(artists),
        "data": artists
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=search)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    """
    Render artist page based on artist id
    :param artist_id: Id of the artist to be displayed
    :return: Artist page
    """
    data = Artist.query.filter_by(id=artist_id).first_or_404()
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    """
    Render form to edit artist
    :param artist_id: Id of the artist to be edited
    :return: Edit artist form page
    """
    form = ArtistForm(request.form)
    artist = Artist.query.filter_by(id=artist_id).first_or_404()
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    """
    Update the artist in database
    :param artist_id: Id of the artist to be updated
    :return: Redirect to the artist's page
    """
    form = ArtistForm(request.form)
    try:
        artist = Artist.query.filter_by(id=artist_id).first_or_404()
        artist.name = form.name.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.genres = form.genres.data
        artist.image_link = form.image_link.data
        artist.facebook_link = form.facebook_link.data
        artist.seeking_venue = form.seeking_venue.data
        artist.seeking_description = form.seeking_description.data
        db.session.commit()
        flash(f'Artist {form.name.data} was successfully edited!')
    except Exception:
        flash(
            f'An error occurred. Artist {form.name.data} could not be edited.')

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    """
    Render form to edit venue
    :param venue_id: Id of the venue to be edited
    :return: Edit venue form page
    """
    form = VenueForm(request.form)
    venue = Venue.query.filter_by(id=venue_id).first_or_404()
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    """
    Update the venue in database
    :param venue_id: Id of the venue to be updated
    :return: Redirect to the venue's page
    """
    form = VenueForm(request.form)
    try:
        venue = Venue.query.filter_by(id=venue_id).first_or_404()
        venue.name = form.name.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.address = form.address.data
        venue.phone = form.phone.data
        venue.genres = form.genres.data
        venue.image_link = form.image_link.data
        venue.facebook_link = form.facebook_link.data
        venue.seeking_talent = form.seeking_talent.data
        venue.seeking_description = form.seeking_description.data
        db.session.commit()
        flash(f'Venue {form.name.data} was successfully edited!')
    except Exception:
        flash(
            f'An error occurred. Venue {form.name.data} could not be edited.')
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    """
    Render form to create artist
    :return: New artist form page
    """
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    """
    Create a new artist in database
    :return: Home page
    """
    form = ArtistForm(request.form)
    try:
        new_artist = Artist(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            genres=form.genres.data,
            image_link=form.image_link.data,
            facebook_link=form.facebook_link.data,
            seeking_venue=form.seeking_venue.data,
            seeking_description=form.seeking_description.data
        )
        db.session.add(new_artist)
        db.session.commit()
        flash(f'Artist {form.name.data} was successfully listed!')
    except Exception:
        flash(
            f'An error occurred. Artist {form.name.data} could not be listed.')

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    """
    Render the shows list page
    :return: Shows list page
    """
    data = [show.complete for show in Show.query.all()]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    """
    Render form to create show
    :return: New show form page
    """
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    """
    Create a new show in database
    :return: Home page
    """
    form = ShowForm(request.form)
    try:
        new_show = Show(
            artist_id=form.artist_id.data,
            venue_id=form.venue_id.data,
            start_time=form.start_time.data
        )
        db.session.add(new_show)
        db.session.commit()
        flash('Show was successfully listed!')
    except Exception:
        flash('An error occurred. Show could not be listed.')

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
