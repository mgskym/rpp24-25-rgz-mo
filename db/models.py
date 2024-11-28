from . import db
from flask_login import UserMixin


class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(102), nullable=False)

    def __repr__(self):
        return f"id:{self.id}, username:{self.username}"


class operations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Numeric, nullable=False)
    category = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(256))
    created_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"id:{self.id}, user_id:{self.user_id}, amount:{self.amount}, created_at:{self.created_at}"


class actions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operation_id = db.Column(db.Integer, nullable=False)
    action_type = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime)

    def __repr__(self):
        return f"id:{self.id}, user_id:{self.user_id}, operation_id:{self.operation_id}, action_type:{self.action_type}, date:{self.date}"
