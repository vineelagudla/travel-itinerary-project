"""Server for travel itinerary application."""

from flask import (Flask, render_template, request, flash, session,
                  redirect)
from model import connect_to_db, db, User, Destination, Experience, Itinerary
import crud
from jinja2 import StrictUndefined

#configuring flask instance and jinja

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

#implementing flask routes

@app.route("/")
def homepage():

    """View homepage"""

    return render_template('homepage.html')


@app.route("/signup")
def signup():

    """Allow user to sign-up"""

    return render_template("signup.html") 

@app.route("/register")
def register():

    """User should be redirected to dashboard after signing up."""

    fname = request.args.get("firstname")
    lname = request.args.get("lastname")
    email = request.args.get("new_email")
    password = request.args.get("password")

    user = User()
    user.fname = fname
    user.lname = lname
    user.email = email
    user.password = password

    db.session.add(user)
    db.session.commit()

    #After user registers, they should be redirected to dashboard

    return render_template("/dashboard.html", fname=fname)

@app.route("/dashboard")
def dashboard():

    """Allow user to view website Dashboard."""
    
    email = request.args.get("email")
    fname = User.query.filter(User.email==email).first().fname
    return render_template('dashboard.html', fname=fname) 

if __name__ == "__main__":
    #connect to db. Else, flask won't be able to access db.
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)