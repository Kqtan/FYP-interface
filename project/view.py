from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from project import db, app
import json
import requests
import pandas as pd
from project.models import *
from flask_login import login_required, current_user
import pickle
from transformers import TFPegasusForConditionalGeneration, AutoTokenizer
import tensorflow as tf
from project.preprocessing import *
from datetime import datetime, timedelta
from nltk.tokenize import word_tokenize

# pegasus = pickle.load(open('pegasus.pkl', 'rb'))
# pegasus_t = pickle.load(open('pegasus_tokenizer.pkl', 'rb'))
pegasus = TFPegasusForConditionalGeneration.from_pretrained('pegasus')
pegasus_t = AutoTokenizer.from_pretrained('google/pegasus-xsum')

with open('lstm_tokenizer.pickle', 'rb') as handle:
    w_tokenizer = pickle.load(handle)

view = Blueprint("view", "__name__")
@view.route("/", methods=["GET", "POST"])
@login_required
def home():
    # if request.method == "POST":
    #     title = request.form.get("title")
    #     msg = request.form.get("message")

    #     if len(msg) < 1 or len(title) <= 0:
    #         flash("The message is too short!", category="error")
    #     else:
    #         # adding the message into the database
    #         # rmb to add the title as well (not done coz still learning)
    #         new_msg = Message(title=title, content=msg, user_id=current_user.user_id)
    #         db.session.add(new_msg)
    #         db.session.commit()

    #         flash("Message added!", category="success")

    return render_template("home.html", user=current_user)

@view.route("/add_new", methods=["GET", "POST"])
@login_required
def add_new():
    if request.method == "POST":
        title = request.form.get("title")
        msg = request.form.get("message")
        submit_type = request.form.get("submit_type")

        if len(msg) < 1 or len(title) <= 0:
            flash("The message is too short!", category="error")
        else:
            # check spam first
            to_predict = title + " " + msg
            spam = predict_spam(to_predict, 125)
            if spam == "Spam":
                flash("Please don't spam me!", category="error")

            else:
                # category prediction
                category = predict_category(to_predict, 40)
                
                if len(word_tokenize(to_predict)) > 50:
                    # expected longest length is 512, sometimes if longer, either truncate or split into smaller segments
                    inputs = pegasus_t(msg, max_length=512, padding="longest", return_tensors="tf", truncation=True)
                    summary_ids = pegasus.generate(inputs["input_ids"], max_length=150, do_sample=False)
                    summary = pegasus_t.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
                else:
                    summary = ""

                # probably let the user choose whether to summarise anot
                new_msg = Message(title=title, content=msg, summary=summary, category=category, user_id=current_user.user_id)
                db.session.add(new_msg)
                db.session.commit()

                flash("Message added and available at the home page!", category="success")

    return render_template("new_msg.html", user=current_user)

@view.route("/delete_msg", methods=["POST"])
@login_required
def delete_msg():
    msg = json.loads(request.data)
    msgId = msg["messageId"]
    msg = Message.query.get(msgId)
    if msg:
        if msg.user_id == current_user.user_id:
            db.session.delete(msg)
            db.session.commit()
    
    return jsonify({})

@view.route("/msg/<id>", methods=["POST", "GET"])
def view_msg1(id):
    msg = Message.query.get(id)
    date_only = msg.date_created.strftime('%Y-%m-%d')
    days = (datetime.now() - msg.date_created).days

    return render_template("view_msg.html", msg=msg, user=current_user, days=days, date=date_only)
