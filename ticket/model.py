from flask import json

from sqlalchemy import Column, Integer, String, Float, LargeBinary
from . import db
import flask_login
import enum

class UserRole(enum.Enum):
    customer = 1
    manager = 2


class User(flask_login.UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(64), unique=False, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    role = db.Column(db.Enum(UserRole), unique=False, nullable=False)

    booked = db.relationship('booking', backref='user', lazy=True)
    

class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240), unique=True, nullable=False)
    director = db.Column(db.String(60), unique=False, nullable=False)
    duration = db.Column(db.Integer, unique=False, nullable=False)
    cast = db.Column(db.String(512), unique=False, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(2048))

    showed = db.relationship('shw', backref='movie', lazy=True)

class Venue(db.Model):
    __tablename__ = "venue"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=False, nullable=False)
    location = db.Column(db.String(60), unique=False, nullable=False)
    num_total_seats = db.Column(db.Integer, unique=False, nullable=False)

    showed = db.relationship('shw', backref='venue', lazy=True)

class shw(db.Model):
    __tablename__ = "shw"
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Date(), unique=False, nullable=False)
    time = db.Column(db.Time(), unique=False, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))

    movie_booked = db.relationship('booking', backref='shw', lazy=True)
  

class booking(db.Model):
    __tablename__ = "booking"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shw_id = db.Column(db.Integer, db.ForeignKey('shw.id'), nullable=False)
    num_seats = db.Column(db.Integer, unique=False, nullable=False)
    date_time = db.Column(db.DateTime(), unique=False, nullable=False)


    
