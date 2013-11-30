from app import db
from datetime import datetime
from flask.ext.sqlalchemy import BaseQuery
from sqlalchemy_searchable import SearchQueryMixin, make_searchable
from sqlalchemy_utils.types import TSVectorType

ROLE_ADMIN = 0
ROLE_USER = 1

make_searchable()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow())
    items = db.relationship('Item', backref='user', lazy='dynamic')
    location_id = db.Column(db.Integer, db.ForeignKey('user_location.id'))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
         return self.username


class ItemQuery(BaseQuery, SearchQueryMixin):
    pass


class Item(db.Model):
    query_class = ItemQuery
    __tablenme__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(80))
    price = db.Column(db.Float)
    description = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('item_location.id'))
    
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0)

    search_vector = db.Column(TSVectorType('name', 'description'))

    def __repr__(self):
        return self.name


class User_location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='user_location', lazy='dynamic')

    def __repr__(self):
        return self.name


class Item_location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    description = db.Column(db.String(200))
    items = db.relationship('Item', backref='item_location', lazy='dynamic')

    def __repr__(self):
        return self.name

