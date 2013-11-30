from flask import render_template, flash, redirect, url_for, session, g, request, jsonify
from flask.ext.login import login_user, logout_user, current_user
from app import app, db, lm
from models import User, Item, User_location, Item_location
from forms import LoginForm, ItemForm, SearchForm
from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash

# TEMP FUNCTION!
def setloc(data, itemOrUser):
    if itemOrUser == 'item':
        
        location = Item_location.query.filter_by(name=data).first()

        if location is None:
            
            location = Item_location( name = data
                                    , latitude = 0
                                    , longitude = 0
                                    , description = "temp"
                                    )
    else: 
        location = Item_location.query.filter_by(name=data).first()

        if location is None:
            
            location = User_location( name = data
                                    , latitude = 0
                                    , longitude = 0
                                    , description = "temp"
                                    )
    db.session.add(location)
    db.session.commit()

    return location.id



@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route("/", methods=["GET", "POST"])
def index():
    title = "Food site"

    form = ItemForm()
    
    if g.user is None or not g.user.is_authenticated():
        user = User.query.filter_by(username="Anonymous").first()
    else:
        user = g.user

    if form.validate_on_submit():

        item = Item( name = form.name.data
                   , price = form.price.data
                   , location_id = setloc(form.location.data, 'item')
                   , description = form.description.data
                   , user = user)

        db.session.add(item)
        db.session.commit()

        flash("Your item has been added!")

        return redirect(url_for("index"))


    items = Item.query.order_by('rating').all()[::-1]

    return render_template( "index.html"
                          , form = form
                          , title = title 
                          , items = items )


@app.route("/login", methods=["GET", "POST"])
def login():
    title = "Login"
    
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
       
        username = form.username.data
        email    = form.email.data
        password = generate_password_hash(form.password.data)
        
        if username == "Anonymous":
            return redirect(url_for("login"))

        user = User.query.filter_by(email=email).first()

        if user == None:
            user = User( username = username
                       , email = email
                       , password = password
                       , location_id = setloc(form.location.data, 'user') )

            db.session.add(user)
            db.session.commit()

        if check_password_hash(user.password, form.password.data):
            
            remember_me = False
            if "rememeber_me" in session:
                remember_me = session["remember me"]
                session.pop("remember_me", None)

            login_user(user, remember=remember_me)
            flash("Hey, " + username + "!")
            
            return redirect(url_for("index"))

        flash("Something went wrong...")

    return render_template( "login.html"
                          , form = form
                          , title = title )

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))



@app.route("/search", methods=["GET", "POST"])
def search():
    
    title = "Search"

    form = SearchForm()
    
    if form.validate_on_submit():
        query = form.query.data
        items = Item.query.search(query).all()

    else:
        items = []

    return render_template( "search.html"
                          , form = form
                          , title = title 
                          , items = items )


@app.route("/vote/<type>/<int:id>")
def vote(type, id):
    
      item = Item.query.get(id)

      if type == 'like':
          item.likes += 1
      else:
          item.dislikes += 1

      item.rating = item.likes - item.dislikes
      
      db.session.commit()

      return redirect(url_for("index"))


@app.route("/remove_vote/<type>/<int:id>")
def remove_vote(type, id):
    
      item = Item.query.get(id)

      if type == 'like':
          item.likes -= 1
          item.rating -= 1
      else:
          item.dislikes -= 1
          item.rating += 1

      item.rating = item.likes - item.dislikes
      
      db.session.commit()
      
      return redirect(url_for("index"))
