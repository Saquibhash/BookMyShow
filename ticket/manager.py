from flask import request, redirect, url_for, render_template, Blueprint, flash
from flask_login import current_user
import flask_login
from . import model
from datetime import date, timedelta
from . import db 
from functools import wraps
from datetime import datetime
from flask.json import jsonify




blue = Blueprint("manager", __name__)

def manager_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != model.UserRole.manager:
            return redirect(url_for('authenticate.login', next=request.url))
        if current_user.role == model.UserRole.manager:
            return f(*args, **kwargs)
    return decorated_function



@blue.route("/schedule")
@flask_login.login_required
@manager_only
def schedule():
    shws, num_results = manager_bookings_aux()
    return render_template("manager_schedule.html", packed=zip(shws, num_results), shws=shws)


@blue.route("/delete/<int:id>")
@flask_login.login_required
@manager_only
def delete(id):
    current_data = model.shw.query.get(id)
    db.session.delete(current_data)
    db.session.commit()
    flash("You have deleted a show", 'success')
    return redirect(url_for("manager.schedule"))


@blue.route("/edit/<int:id>")
@flask_login.login_required
@manager_only
def edit(id):
    movies = model.Movie.query.all()
    venues = model.Venue.query.all()
    current_data = model.shw.query.get(id)
    return render_template("manager_edit.html", movies=movies, venues=venues, current_data=current_data)


@blue.route("/edit/<int:id>", methods=["POST"])
@flask_login.login_required
@manager_only
def edit_post(id):
    movie = request.form.get("movie")
    venue = request.form.get("venue")
    day = request.form.get("day")
    time = request.form.get("time")
   
    day = datetime.strptime(day, "%Y-%m-%d").date()
    time = datetime.strptime(time, "%H:%M:%S").time()

    shw = model.shw.query.filter(model.shw.id == id).first()
    shw.day = day
    shw.time = time
    shw.movie_id = movie
    shw.venue_id = venue 

    db.session.commit()
    flash("You have edited a show", 'success')
    return redirect(url_for("manager.schedule"))



@blue.route("/add")
@flask_login.login_required
@manager_only
def add():
    movies = model.Movie.query.all()
    venues = model.Venue.query.all()
    current_day = date.today().strftime('%Y-%m-%d')
    return render_template("manager_add.html", movies=movies, venues=venues, current_day=current_day)

@blue.route("/add", methods=["POST"])
@flask_login.login_required
@manager_only
def add_post():
    movie = request.form.get("movie")
    venue = request.form.get("venue")
    day = request.form.get("day")
    time = request.form.get("time")
    time = time + ':00'
    day = datetime.strptime(day, "%Y-%m-%d").date()
    time = datetime.strptime(time, "%H:%M:%S").time()
    new_shw = model.shw(day=day, time=time, movie_id=movie, venue_id=venue)
    db.session.add(new_shw)
    db.session.commit()
    return redirect(url_for("manager.schedule"))

@blue.route("/venue")
@flask_login.login_required
@manager_only
def list_venues():
    venues = model.Venue.query.all()
    return render_template("manager_venue.html", venues=venues)

@blue.route("/create", methods=["GET","POST"])
@flask_login.login_required
@manager_only
def create_venue():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        num_total_seats = request.form.get("num_total_seats")
        new_venue = model.Venue(name=name, location=location, num_total_seats=num_total_seats)
        db.session.add(new_venue)
        db.session.commit()
        flash("New venue added successfully!", "success")   
        return redirect(url_for("manager.list_venues"))

    return render_template('manager_vcreate.html')

@blue.route("/edit_venue/<int:venue_id>", methods=["GET", "POST"])
@flask_login.login_required
@manager_only
def edit_venue(venue_id):
    venue = model.Venue.query.get(venue_id)
    if request.method == 'POST':
        venue.name = request.form.get('name')
        venue.location = request.form.get('location')
        venue.num_total_seats = request.form.get("num_total_seats")
        db.session.commit()
        flash('Venue updated successfully!')
        return redirect(url_for('manager.list_venues'))

    return render_template('manager_vedit.html', venue=venue)


@blue.route("/delete_venue/<int:venue_id>", methods=["GET", "POST"])
@flask_login.login_required
@manager_only
def delete_venue(venue_id):
    venue = model.Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue deleted successfully!')
    return redirect(url_for("manager.list_venues"))
    



@blue.route("/movie")
@flask_login.login_required
@manager_only
def list_movies():
    movies = model.Movie.query.all()
    return render_template('manager_movie.html',  movies=movies)


@blue.route('/create_movie', methods=['GET', 'POST'])
@flask_login.login_required
@manager_only
def create_movie():
    if request.method == 'POST':
        title = request.form['title']
        director = request.form['director']
        duration = request.form['duration']
        cast = request.form['cast']
        rating = request.form['rating']
        price = request.form['price']
        img = request.form['img']   
        new_movie = model.Movie(title=title, director=director, duration=duration, cast=cast, rating=rating, price=price, img=img)
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('manager.list_movies'))
    
    return render_template('manager_mcreate.html' )

@blue.route("/edit_movie/<int:movie_id>", methods=["GET", "POST"])
@flask_login.login_required
@manager_only
def edit_movie(movie_id):
    movie = model.Movie.query.get(movie_id)
    if request.method == 'POST':
        movie.title = request.form.get('title')
        movie.director = request.form.get('director')
        movie.duration = request.form.get('duration')
        movie.cast = request.form.get('cast')
        movie.rating = request.form.get('rating')
        movie.price = request.form.get('price')
        movie.img = request.form.get('img')
        
        db.session.commit()
        return redirect(url_for('manager.list_movies'))

    
    return render_template('manager_medit.html', movies=movie, movie=movie)


@blue.route("/delete_movie/<int:movie_id>", methods=["GET", "POST"])
@flask_login.login_required
@manager_only
def delete_movie(movie_id):
    movie = model.Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('manager.list_movies'))

@blue.route("/bookings")
@flask_login.login_required
@manager_only
def bookings():
    shws, num_results = manager_bookings_aux()
    return render_template("manager_bookings.html", packed=zip(shws, num_results), shws=shws)


@blue.route("/manager_booking/<int:id>")
@flask_login.login_required
@manager_only
def manager_booking(id):
    bookings = model.booking.query.filter(model.booking.shw_id == id).order_by(model.booking.date_time).all()
    return render_template("manager_booking.html", bookings=bookings)


def manager_bookings_aux():
    current_day = date.today()
    future = current_day + timedelta(days=7)
    past = current_day - timedelta(days=7)
    shws = model.shw.query.filter(model.shw.day <= future, model.shw.day >= past).order_by(model.shw.day.asc(), model.shw.time.asc()).all()
    num_results = []
    for sh in shws:
        num_results.append(sh.venue.num_total_seats - compute_reserved_seats(sh.id))
    return shws, num_results


def compute_reserved_seats(id):
    shw = model.shw.query.filter(model.shw.id == id).one()
    sum_result = db.session.query(
        db.func.sum(model.booking.num_seats).label('reserved')
    ).filter(
        model.booking.shw == shw
    ).one()
    num_reserved_seats = sum_result.reserved
    if (sum_result.reserved != None):
        num_free_seats = shw.venue.num_total_seats - num_reserved_seats
    else:
        num_free_seats = shw.venue.num_total_seats         
    return  num_free_seats

@blue.route('/ajax', methods=['POST', 'GET'])
def process_ajax():
    if request.method == "POST":
        shws = model.shw.query.all()

        results = {}
        for sh in shws:
            seats = compute_reserved_seats(sh.id)
            results[sh.id] = seats
        result = results
    return jsonify(result=result)


