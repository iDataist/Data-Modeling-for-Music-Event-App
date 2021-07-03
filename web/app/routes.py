
from flask import render_template, request, flash, redirect, url_for, jsonify, abort
import dateutil.parser
import babel
from logging import Formatter, FileHandler
from app.forms import *
from app import app, db
from app.models import Venue, Artist, Show
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime

engine = create_engine('postgresql://postgres:postgres@localhost:5432/fyyur',
                       echo=False)

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

@app.route('/')
def index():
    return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    venues = pd.read_sql("SELECT city, state, id, name FROM venue", engine)
    data = venues.to_dict(orient='records')
    return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
    venues = pd.read_sql("SELECT id, name FROM venue", engine)
    search_term = request.form.get('search_term')
    data = venues.loc[venues['name'] \
                 .str.contains(search_term, case=False)] \
                 .to_dict(orient='records')
    return render_template('pages/search_venues.html', 
                            areas=data, 
                            count=len(data), 
                            search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue_subset = pd.read_sql("SELECT * FROM venue where id = {}".format(venue_id),
                               engine)
    show_subset = pd.read_sql("SELECT venue_id, artist_id, start_time FROM show",
                              engine)
    artist_subset = pd.read_sql("SELECT id, image_link, name FROM artist",
                                engine)
    venue_show_df = pd.merge(venue_subset['id'], 
                             show_subset, 
                             left_on='id', 
                             right_on='venue_id', 
                             how='left')
    venue_show_df['is_upcoming'] = venue_show_df['start_time'] \
      .apply(lambda x: 1 if x > datetime.utcnow() else 0)
    venue_show_df['is_past'] = venue_show_df['start_time'] \
      .apply(lambda x: 1 if x < datetime.utcnow() else 0)
    show_count_df = venue_show_df.groupby('id') \
                                 .agg({'is_upcoming': 'sum', 'is_past': 'sum'}) \
                                 .reset_index()
    show_count_df.columns = ['id', 'upcoming_shows_count', 'past_shows_count']
    venues = pd.merge(venue_subset, 
                      show_count_df, 
                      on='id', 
                      how='left')
    data = venues.to_dict(orient='records')

    venue_show_artist_df = pd.merge(venue_show_df, 
                                    artist_subset, 
                                    left_on='artist_id', 
                                    right_on='id', 
                                    how='left')
    columns = ['artist_id', 'image_link', 'name', 'start_time']
    upcoming_shows = venue_show_artist_df \
                     .loc[venue_show_artist_df.is_upcoming == 1][columns] \
                     .to_dict(orient='records')
    past_shows = venue_show_artist_df \
                 .loc[venue_show_artist_df.is_past == 1][columns] \
                 .to_dict(orient='records')

    return render_template('pages/show_venue.html', 
                           venue=data[0], 
                           upcoming_shows=upcoming_shows,
                           past_shows=past_shows)

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    venue = Venue()
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.genre = request.form['genre']
    venue.facebook_link = request.form['facebook_link']
    venue.image_link = request.form['image_link']
    venue.website_link = request.form['website_link']
    if request.form['seeking_talent'] == 'y':
      venue.seeking_talent = True
    else:
      venue.seeking_talent = False
    try:
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        return redirect('/forms/new_venue')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Venue ' \
              + request.form['name'] \
              + ' could not be listed.')
        app.logger.error(e)
    return render_template('pages/home.html')

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue_subset = pd.read_sql("SELECT id, name FROM venue where id = {}" \
                   .format(venue_id), engine) \
                   .to_dict(orient='records')
  return render_template('forms/edit_venue.html', 
                         form=form, 
                         venue=venue_subset)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)
    app.logger.debug(venue)
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.genre = request.form['genre']
    venue.facebook_link = request.form['facebook_link']
    venue.image_link = request.form['image_link']
    venue.website_link = request.form['website_link']
    if request.form['seeking_talent'] == 'y':
      venue.seeking_talent = True
    else:
      venue.seeking_talent = False

    try:
        db.session.update(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
        # return redirect('/venues/<int:venue_id>/edit')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Venue ' \
              + request.form['name'] \
              + ' could not be updated.')
        app.logger.error(e)
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    error = False
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
    except():
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({'success': True})

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = pd.read_sql("SELECT id, name FROM artist", engine)
  data = artists.to_dict(orient='records')
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  artists = pd.read_sql("SELECT id, name FROM artist", engine)
  search_term = request.form.get('search_term')
  data = artists.loc[artists['name'] \
                .str.contains(search_term, case=False)] \
                .to_dict(orient='records')
  return render_template('pages/search_artists.html', 
                         areas=data,
                         count=len(data),
                         search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist_subset = pd.read_sql("SELECT * FROM artist where id = {}".format(artist_id),
                                engine)
    show_subset = pd.read_sql("SELECT venue_id, artist_id, start_time FROM show",
                              engine)
    venue_subset = pd.read_sql("SELECT id, image_link, name FROM venue",
                               engine)
    artist_show_df = pd.merge(artist_subset['id'], 
                            show_subset, 
                            left_on='id', 
                            right_on='artist_id', 
                            how='left')
    artist_show_df['is_upcoming'] = artist_show_df['start_time'] \
      .apply(lambda x: 1 if x > datetime.utcnow() else 0)
    artist_show_df['is_past'] = artist_show_df['start_time'] \
      .apply(lambda x: 1 if x < datetime.utcnow() else 0)
    show_count_df = artist_show_df.groupby('id') \
                                .agg({'is_upcoming': 'sum', 'is_past': 'sum'}) \
                                .reset_index()
    show_count_df.columns = ['id', 'upcoming_shows_count', 'past_shows_count']
    artists = pd.merge(artist_subset, 
                      show_count_df, 
                      on='id', 
                      how='left')
    data = artists.to_dict(orient='records')

    artist_show_venue_df = pd.merge(artist_show_df , 
                                    venue_subset, 
                                    left_on='venue_id', 
                                    right_on='id', 
                                    how='left') 
    columns = ['venue_id', 'image_link', 'name', 'start_time']
    upcoming_shows = artist_show_venue_df \
                    .loc[artist_show_venue_df.is_upcoming == 1][columns] \
                    .to_dict(orient='records')
    past_shows = artist_show_venue_df \
                .loc[artist_show_venue_df.is_past == 1][columns] \
                .to_dict(orient='records')
    return render_template('pages/show_artist.html',
                           artist=data[0], 
                           upcoming_shows=upcoming_shows,
                           past_shows=past_shows)

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    artist = Artist()
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.address = request.form['address']
    artist.phone = request.form['phone']
    artist.genre = request.form['genre']
    artist.facebook_link = request.form['facebook_link']
    artist.image_link = request.form['image_link']
    artist.website_link = request.form['website_link']
    if request.form['seeking_venue'] == 'y':
      artist.seeking_venue = True
    else:
      artist.seeking_venue = False
    try:
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully updated!')
        return redirect('/forms/new_artist')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Artist ' \
              + request.form['name'] \
              + ' could not be updated.')
        app.logger.error(e)
    return render_template('pages/home.html')

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist_subset = pd.read_sql("SELECT id, name FROM artist where id = {}" \
                    .format(artist_id),engine) \
                    .to_dict(orient='records')
  return render_template('forms/edit_artist.html', 
                         form=form, 
                         artist=artist_subset)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist = Artist.query.get(artist_id)
    app.logger.debug(artist)
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.address = request.form['address']
    artist.phone = request.form['phone']
    artist.genre = request.form['genre']
    artist.facebook_link = request.form['facebook_link']
    artist.image_link = request.form['image_link']
    artist.website_link = request.form['website_link']
    if request.form['seeking_venue'] == 'y':
      artist.seeking_venue = True
    else:
      artist.seeking_venue = False

    try:
        db.session.update(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully updated!')
        # return redirect('/artists/<int:artist_id>/edit')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Artist ' \
              + request.form['name'] \
              + ' could not be updated.')
        app.logger.error(e)
    return render_template('pages/home.html')

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    error = False
    try:
        artist = Artist.query.get(artist_id)
        db.session.delete(artist)
        db.session.commit()
    except():
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({'success': True})

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    artist_subset = pd.read_sql("SELECT id, name, image_link FROM artist",
                                engine)
    show_subset = pd.read_sql("SELECT venue_id, artist_id, start_time FROM show",
                              engine)
    venue_subset = pd.read_sql("SELECT id, name FROM venue",
                               engine)
    show_artist_df = pd.merge(show_subset,
                              artist_subset, 
                              left_on='artist_id', 
                              right_on='id', 
                              how='left').drop(columns=['id'])
    show_artist_venue_df = pd.merge(show_artist_df, 
                                    venue_subset,
                                    left_on='venue_id', 
                                    right_on='id', 
                                    how='left').drop(columns=['id'])
    show_artist_venue_df.columns = ['venue_id', 'artist_id', 'start_time', \
      'artist_name', 'artist_image_link', 'venue_name']
    data = show_artist_venue_df.to_dict(orient='records')
    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    show = Show()
    show.artist_id = request.form['artist_id']
    show.venue_id = request.form['venue_id']
    show.start_time = request.form['start_time']
    try:
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully updated!')
        return redirect('/forms/new_show')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Artist ' \
              + request.form['name'] \
              + ' could not be updated.')
        app.logger.error(e)
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


# if not app.debug:
#     file_handler = FileHandler('error.log')
#     file_handler.setFormatter(
#         Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
#     )
#     app.logger.setLevel(logging.INFO)
#     file_handler.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler)
#     app.logger.info('errors')