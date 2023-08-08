# the main script to collect all the necessary blueprints
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_cors import CORS, cross_origin
import path
from flask_login import LoginManager, current_user

DB_NAME = "final.db"
app = Flask(__name__)

# the emphasis on security configuration
# https://pythonhosted.org/Flask-Security/index.html
# security should be our utmost priority
app.config["SECRET_KEY"] = "/A%D*G-KaPdSgVkYp3s6v9y$B&E(H+MbQeThWmZq4t7w!z%C*F-J@NcRfUjXn2r5"
app.config['SQLALCHEMY_DATABASE_URI'] = "the location"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
CORS(app, supports_credentials=True)
#supports_credentials=True, 
db = SQLAlchemy(app)
ma = Marshmallow(app)

# FLASK MAIL config
# initiate sending email configurations
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587 #587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
#app.config["MAIL_DEFAULT_SENDER"] = set the default address
app.config["MAIL_USERNAME"] = "your email"
app.config["MAIL_PASSWORD"] = "password"

mail = Mail(app)

from project.view import view
from project.auth import auth
from project.profile import user
from project.contactus import contact

app.register_blueprint(view, url_prefix="/view")
app.register_blueprint(auth, url_prefix="/a")
app.register_blueprint(contact, url_prefix="/contact")
app.register_blueprint(user, url_prefix="/u")

# landing page
@app.route("/", methods=["GET"])
def landing():
    return render_template("landing_page.html", user=current_user)

from project.models import *

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# use this function to load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))