#!/usr/bin/env python
from app import db
from app.models import User, User_location, Item_location, ROLE_ADMIN
from werkzeug import generate_password_hash

user_loc = User_location(name="Fallmouth and Keogh Halls", latitude=51.498677, longitude=-0.173056, description="One of the Halls of residence at Southside, Imperial College.")

db.session.add(user_loc)
db.session.commit()



shop = Item_location(name="Sainsbury's, Cromwell Rd", latitude=51.494834, longitude=-0.188656, description="Sainsbury's Superstore")

db.session.add(shop)
db.session.commit()



pw = generate_password_hash("//Fyjb572nqpr1")

admin = User(username="JCGrant", email="jamescolin.grant@gmail.com", password=pw, location_id=1, role=0)

db.session.add(admin)
db.session.commit()



anon = User(username="Anonymous")

db.session.add(anon)
db.session.commit()

