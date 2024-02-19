from flask import request, redirect, url_for, render_template, Blueprint
from flask_login import current_user
import flask_login
from . import model
from datetime import date, timedelta
from . import db 
from functools import wraps
from datetime import datetime
from flask.json import jsonify

blue = Blueprint("aux", __name__)

def manager_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != model.UserRole.manager:
            return redirect(url_for('authenticate.login', next=request.url))
        if current_user.role == model.UserRole.manager:
            return f(*args, **kwargs)
    return decorated_function

def manager_bookings_aux():
    current_day = date.today()
    future = current_day + timedelta(days=7)
    past = current_day - timedelta(days=7)
    shws= model.shw.query.filter(model.shw.day <= future, model.shw.day >= past).order_by(model.shw.day.asc(), model.shw.time.asc()).all()
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