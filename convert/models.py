
from convert import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    results = db.relationship('Convert', backref='user', lazy=True)

    def __repr__(self):
        return f"User:'{self.email}'"


class Convert(db.Model, UserMixin):
    __tablename__ = 'converts'
    id = db.Column(db.Integer, primary_key=True)
    value_dec = db.Column(db.String())
    value_bin = db.Column(db.String())
    value_hex = db.Column(db.String())
    base = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),  nullable=False)

    def __repr__(self):
        return f"Value:'{self.id}'"
