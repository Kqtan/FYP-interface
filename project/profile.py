from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from project import db, app
import json
import requests
import pandas as pd
from project.models import *
from flask_login import current_user
from collections import Counter

user = Blueprint("u", "__name__")
@user.route("/", methods=["GET"])
def profile():
    messages = Message.query.filter_by(user_id=current_user.user_id).all()
    msg_len = len(messages)

    day = (datetime.now() - messages[0].date_created).days

    category_counts = dict(Counter(msg.category for msg in messages))
    # category_counts_json = json.dumps(category_counts)
    # category_counts['Total'] = msg_len

    return render_template("profile.html", user=current_user, category_counts=category_counts, msg_len=msg_len, day=day)
