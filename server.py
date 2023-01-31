"""Server for travel itinerary application."""

from flask import (Flask, render_template, request, flash, session,
                  redirect, jsonify)
from model import connect_to_db, db
import crud
import yelp_api
from jinja2 import StrictUndefined

#configuring flask instance and jinja

app = Flask(__name__)
# Required to use Flask sessions
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

#implementing flask routes

@app.route("/")
def homepage():

    """View homepage."""

    # Redirect to dashbord if there is active user in session
    if "user" in session and session["user"] != None:
        return redirect("/dashboard")

    return render_template('homepage.html')


@app.route("/signin")
def signin():

    """Allow user to login."""
    #TODO need to do user validitaion
    email = request.args.get("email")
    user_info = crud.get_user_details(email)
    session["user"] = user_info
    session.modified = True

    return redirect("/dashboard")


@app.route("/signup")
def signup():

    """Allow user to sign-up."""

    # Redirect to dashbord if there is active user in session
    if "user" in session and session["user"] != None:
        return redirect("/dashboard")

    return render_template("signup.html") 

@app.route("/register")
def register():

    """User should be redirected to dashboard after signing up."""
    #TODO need to do user validitaion
    fname = request.args.get("firstname")
    lname = request.args.get("lastname")
    email = request.args.get("new_email")
    password = request.args.get("password")

    crud.create_user(fname, lname, email, password)
    user_info = crud.get_user_details(email)
    session["user"] = user_info
    session.modified = True

    #After user registers, they should be redirected to dashboard

    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():

    """Allow user to view website Dashboard."""

    if "user" not in session or session["user"] == None:
        return redirect("/")
    
    user = session["user"]

    return render_template('dashboard.html', fname = user["fname"])


@app.route("/logout")
def logout():

    """Logout functionality."""

    session["user"] = None
    session.modified = True

    return redirect("/")


@app.route("/itinerary")
def create_itinerary():

    """Show itinerary landings page."""

    if "user" not in session or session["user"] == None:
        return redirect("/")
 
    return render_template('itinerary.html')


@app.route("/itinerary-form")
def itinerary_form():
    #Fetch itinerary_details from the form and store it in db
    if "user" not in session or session["user"] == None:
        return redirect("/")
    
    user_id = session["user"]["user_id"]
    itn_name = request.args.get("itn_name")
    location = request.args.get("itn_location")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    itn_id = crud.create_itinerary(itn_name, user_id, location, start_date, end_date).itinerary_id
    session["itinerary_id"] = itn_id
    session.modified = True

    return redirect("/search")

@app.route("/search")
def search():

    if "user" not in session or session["user"] == None:
        return redirect("/")

    if "itinerary_id" not in session or session["itinerary_id"] == None:
        return redirect("/itinerary-form")

    itn_id = session["itinerary_id"]

    return render_template('search.html')


@app.route("/load-itinerary")
def load_itinerary():

    """User should be able to see their itineraries."""

    exp_name = request.args.get("name")
    reviews = request.args.get("reviews")
    location = request.args.get("location")
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    itn_id = session["itinerary_id"]
    crud.create_experience(exp_name, itn_id, location, latitude, longitude)

    return jsonify([exp_name])


@app.route("/search-results")
def search_results():
    location = request.args.get("location")
    results = yelp_api.get_activities(location)
    return jsonify(results)


if __name__ == "__main__":
    #connect to db. Else, flask won't be able to access db.
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)