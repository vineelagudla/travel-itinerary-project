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


@app.route("/signin", methods = ["POST"])
def signin():

    """Allow user to login."""
    #TODO need to do user validitaion
    email = request.form.get("email")
    password = request.form.get("password")
    user_info = crud.get_user_details(email)

    if(not user_info):
         flash("User does not exist!") 

         return redirect("/")

    elif (email != user_info["email"] or password != user_info["password"]):
         flash("You have entered incorrect password. Try again!") 

         return redirect("/")

    else:
        flash("You have logged in succesfully!") 
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
    user_id = user["user_id"]

    itn_count = crud.get_itinerary_count(user_id)

    shared_itn_count = crud.get_shared_itinerary_count(user_id)

    return render_template('dashboard.html', fname = user["fname"], itn_count=itn_count, shared_itn_count=shared_itn_count)


@app.route("/logout")
def logout():

    """Logout functionality."""

    session["user"] = None
    session.modified = True

    return redirect("/")


@app.route("/create-itinerary")
def create_itinerary():

    """Show itinerary landings page."""

    if "user" not in session or session["user"] == None:
        return redirect("/")
 
    return render_template('create-itinerary.html')


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
    share_itn = request.args.get("share")

    itn_id = crud.create_itinerary(itn_name, user_id, location, start_date, end_date, share_itn).itinerary_id
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

    """User should be able to load the experience info in experiences and destinations tables."""

    #Fetch exp and destination details from the search display results and store it in db
    exp_name = request.args.get("name")
    reviews = request.args.get("reviews")
    location = request.args.get("location")
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    itn_id = session["itinerary_id"]
    crud.create_experience(exp_name, itn_id, location, latitude, longitude)

    return jsonify([exp_name])


@app.route("/view-itineraries")
def view_itineraries():

    """User should be able to view their respective owned itineraries."""

    user_id = session["user"]["user_id"]
    itn_lst = crud.get_user_itineraries(user_id)

    return render_template('view-itineraries.html', itn_lst=itn_lst)

@app.route("/show_itinerary")
def show_itinerary():

    """Show the details of the selected itinerary"""

    itn_id = request.args.get("itn_id")
    itn_info = crud.get_itinerary_details(itn_id)

    return render_template('show-itinerary.html', itn_info=itn_info)


@app.route("/shared-itineraries")
def shared_itineraries():

    """Show list of shared itineraries."""

    user_id =session["user"]["user_id"]
    shared_itns = crud.get_shared_itineraries(user_id)

    return render_template('shared-itineraries.html', shared_itns=shared_itns)


@app.route("/search-results")
def search_results():
    location = request.args.get("location")
    results = yelp_api.get_activities(location)
    return jsonify(results)


if __name__ == "__main__":
    #connect to db. Else, flask won't be able to access db.
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)