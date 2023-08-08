from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from project import db, app
import json
import requests
import pandas as pd
from project.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", "__name__")
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("view.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exist.", category="error")

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email already exists.", category="error")
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category="error")
        elif len(firstName) < 2:
            flash('First name must be greater than 1 characters.', category="error")
        elif password1 != password2:
            flash('Password don\'t match.', category="error")
        elif len(password1) < 8:
            flash('Password must be at least 8 characters', category="error")
        else:
            # add user into the database
            new_user = User(email=email, username=username, name=firstName, password=generate_password_hash(password1, method="scrypt"))
            db.session.add(new_user)
            db.session.commit()

            flash('Account created! Login Now!', category="success")
            # url for blueprint view, and function name 'home'
            return redirect(url_for("auth.login"))

    return render_template("sign_up.html", user=current_user)