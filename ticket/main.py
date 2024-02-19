from datetime import date, datetime, timedelta
import dateutil.tz
import sqlite3
from flask import Blueprint, render_template, request, flash, url_for, redirect
import flask_login
from flask_login import current_user 
from sqlalchemy import func
from . import model
from . import db
from .model import Movie, Venue, shw


blue = Blueprint("main", __name__)

@blue.route("/")
def index():
    current_day = date.today()
    
    future = current_day + timedelta(days=7)
    amovies = model.shw.query.filter(model.shw.day > current_day, model.shw.day <= future).order_by(model.shw.day.asc(), model.shw.time.asc()).all()
    bmovies = model.shw.query.filter(model.shw.day == current_day).order_by(model.shw.time.asc()).all()
    movies = model.Movie.query.all()
    users = model.User.query.all() 
    return render_template("main/index.html", all_movies=movies, users=users, next_shws=amovies, today_shws=bmovies)

@blue.route("/movie/<int:id>")
def movie(id):
    movie = model.Movie.query.get(id)
    current_day = date.today()

    shws = model.shw.query.filter(model.shw.movie_id == id, model.shw.day >= current_day).order_by(model.shw.day.asc(), model.shw.time.asc()).all()
    return render_template("movie.html", movie=movie, shws=shws)

@blue.route("/user")
@flask_login.login_required
def user():
    current_day = date.today()
    now = []
    past = []
    now_bookings = model.booking.query.filter(model.booking.user_id == current_user.id).order_by(model.booking.date_time).all()
    for res in now_bookings:
        if res.shw.day >= current_day:
            now.append(res)
        else:
            past.append(res)
    return render_template('user.html', now_bookings = now, past_bookings = past)


@blue.route("/booking/", defaults={'id': None})
@blue.route("/booking/<int:id>")
@flask_login.login_required
def booking(id):
    current_day = date.today()
    current_time = datetime.now()
    all_shws = model.shw.query.filter(model.shw.day >= current_day).order_by(model.shw.day.asc(), model.shw.time.asc()).all()
    if id == None:
        return render_template("booking.html", shw=None, shws=all_shws)
    else:
        shw = model.shw.query.get(id)
        shws = model.shw.query.filter(model.shw.movie_id == shw.movie_id, model.shw.day >= current_day).order_by(model.shw.day.asc(), model.shw.time.asc()).all()
        return render_template("booking.html", shw=shw, shws=shws)


@blue.route("/booking/", methods=["POST"])
@flask_login.login_required
def booking_post():
    choosen_shw = request.form.get("shw") 
    choosen_num_seats = request.form.get("seats")


    shw = model.shw.query.get(choosen_shw)

    new_booking = model.booking(user_id=current_user.id, shw_id=shw.id, num_seats=int(choosen_num_seats), date_time=datetime.now())
    
    db.session.add(new_booking)
    db.session.commit()
    flash("You have bought %s tickets for %s"%(choosen_num_seats, shw.movie.title), 'success')
    return redirect(url_for("main.index"))


@blue.route('/search')
def search():
    query = request.args.get('query', '')
    movies = Movie.query.filter((Movie.title.like(f'%' + query.lower() + '%')) | (Movie.rating == query)).all()
    venues = Venue.query.filter(Venue.location.like(f'%' + query + '%')).all()
    return render_template('search.html', query=query, movies=movies, venues=venues)