from marshmallow import Schema,fields
from sqlalchemy import schema
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True)
    email = db.Column(db.String(255), unique=True, index=True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User {self.username}'

class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    artist = db.Column(db.String())
    urlToCover = db.Column(db.String())

    def __repr__(self):
        return self.title

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def get_by_id(cls,id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
            
class SongSchema(Schema):
    id = fields.Integer()
    title =fields.String()
    artist =fields.String()
    urlToCover =fields.String()
