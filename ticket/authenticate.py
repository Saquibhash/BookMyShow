from flask import Blueprint, render_template, request, redirect, url_for, flash
import flask_login
from . import db, bcrypt
from . import model

blue = Blueprint("authenticate", __name__)

@blue.route("/signup")
def signup():
    return render_template("authenticate/signup.html")


@blue.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role")

    if password != request.form.get("password_repeat"):
        flash("Passwords are different. Try again.", 'error')
        return redirect(url_for("authenticate.signup"))

    if role == 'manager' and (email != "test@test.com" and email != "manager@bms.com"): 
        flash("You cannot Sign Up as a manager", 'error')
        return redirect(url_for("authenticate.signup"))
    
    user = model.User.query.filter_by(email=email).first()
    if user:
        flash("Email you provided is already registered.", 'error')
        return redirect(url_for("authenticate.signup"))
 
    if role == 'manager':
        role = model.UserRole.manager
    else:
        role = model.UserRole.customer

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = model.User(email=email, name=username, password=password_hash, role=role)
    db.session.add(new_user)
    db.session.commit()
    flash("You have successfully signed up!", 'success')
    return redirect(url_for("authenticate.login"))


@blue.route("/login")
def login():
    return render_template("authenticate/login.html")


@blue.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")   
    user = model.User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        flask_login.login_user(user)
        flash("You have successfully loged!", 'success')
        return redirect(url_for("main.index"))
    else:
        if user == None:
            flash("User not registered. Go to Sign Up.", 'error')
            return redirect(url_for("authenticate.login"))
        if user.email == email and bcrypt.check_password_hash(user.password, password) == 0:
            flash("Wrong password", 'error')
        return redirect(url_for("authenticate.login"))

@blue.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    flash ('You have been logged out', 'success')
    return redirect(url_for("authenticate.login"))
