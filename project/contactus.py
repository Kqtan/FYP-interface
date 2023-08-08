from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from project import db, app, mail
import json
import requests
import pandas as pd
from project.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from datetime import datetime

contact = Blueprint("contact", "__name__")

@contact.route("/", methods=["GET", "POST"])
def contactUs():
    if request.method == "POST":
        subject = request.form.get("subject")
        body = request.form.get("message")
        date_only = datetime.now().strftime('%Y-%m-%d')
        if current_user:
            report = current_user.name + "\n" + current_user.email + "\n" + "Date created: " + date_only + "\n"
        else:
            name = request.form.get("name")
            email = request.form.get("email")
            report = name + "\n" + email + "\n" + "Date created: " + date_only + "\n"

        body = report + body
        print(body)

        msg = Message(subject=subject, body=body, sender="kqtan99@outlook.com", recipients=["kqtan88@gmail.com"])
        mail.send(msg)

        flash("Your feedbacks sent to the developers! Arigatou gozaimasu!")

    return render_template("contact.html", user=current_user)
