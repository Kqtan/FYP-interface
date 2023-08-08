from project import db, ma
from datetime import datetime, timedelta
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "User"
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    username = db.Column(db.String(50))
    name = db.Column(db.String(500), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    message = db.relationship("Message")

    def __init__ (self, email, username, name, password):
        self.email = email
        self.username = username
        self.name = name
        self.password = password
    
    def get_id(self):
        return (self.user_id)

class UserSchema(ma.Schema):
    class Meta:
        fields=('user_id', 'email', 'username', 'name', "password")

#Initialize Schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Message(db.Model):
    __tablename__ = "Message"
    message_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(10000))
    summary = db.Column(db.String(5000))
    category = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__ (self, title, content, summary, category, user_id):
        self.title = title
        self.content = content
        self.summary = summary
        self.category = category
        self.user_id = user_id

class MessageSchema(ma.Schema):
    class Meta:
        fields=('message_id', 'title', 'content', 'summary', 'category', 'user_id', "date_created")

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)