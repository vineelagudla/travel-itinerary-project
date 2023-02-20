"""Server for travel itinerary application."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db
import crud
import yelp_api
from pprint import pprint
from jinja2 import StrictUndefined
import json
from passlib.hash import argon2

# configuring flask instance and jinja
app = Flask(__name__)
# Required to use Flask sessions
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# implementing flask routes


@app.route("/")
def homepage():
    """View homepage."""

    # Redirect to dashbord if there is active user in session
    if "user" in session and session["user"] != None:
        return redirect("/dashboard")

    return render_template('homepage.html')


@app.route("/signin", methods=["POST"])
def signin():
    """Allow user to login."""

    email = request.form.get("email")
    password = request.form.get("password")
    user_info = crud.get_user_details(email)
    hashed_password = user_info["password"]

    # TODO: use password hash only
    verified_password = False
    try:
        verified_password = argon2.verify(password, hashed_password)
    except ValueError as ve:
        verified_password = password == user_info["password"]

    if (not user_info):
        flash("User does not exist!")

        return redirect("/")

    elif email != user_info["email"] or not verified_password:

        flash("You have entered incorrect password. Try again!")

        return redirect("/")

    else:
        session["user"] = user_info
        session.modified = True

        return redirect("/dashboard")


@app.route("/user-profile")
def user_profile():
    """User profile details"""

    if "user" in session and session["user"] != None:
        fname = session["user"]["fname"]
        lname = session["user"]["lname"]
        email = session["user"]["email"]

    return render_template("user-profile.html", fname=fname, lname=lname, email=email)


@app.route("/signup")
def signup():
    """Allow user to sign-up."""

    # Redirect to dashbord if there is active user in session
    if "user" in session and session["user"] != None:
        return redirect("/dashboard")

    return render_template("signup.html")


@app.route("/register", methods=["POST"])
def register():
    """User should be redirected to dashboard after signing up."""

    fname = request.form.get("firstname")
    lname = request.form.get("lastname")
    email = request.form.get("new_email")
    password = request.form.get("password")

    user_info = crud.get_user_details(email)
    hashed = argon2.hash(password)

    if (not user_info):
        
        crud.create_user(fname, lname, email, hashed)
        user_info = crud.get_user_details(email)

        session["user"] = user_info
        session.modified = True

        # After user registers, they should be redirected to dashboard
        return redirect("/dashboard")

    else:
        flash("Email already exists! Try a new one.")

        return redirect("/signup")


@app.route("/dashboard")
def dashboard():
    """Allow user to view website Dashboard."""

    if "user" not in session or session["user"] == None:

        return redirect("/")

    user = session["user"]
    user_id = user["user_id"]

    owned_itn_count = crud.get_itinerary_count(user_id)
    public_itn_count = crud.get_public_itinerary_count(user_id)
    friends_itn_count = crud.get_friends_itinerary_count(user_id)
    lname = session["user"]["lname"]
    email = session["user"]["email"]

    return render_template('dashboard.html', fname=user["fname"], owned_itn_count=owned_itn_count, public_itn_count=public_itn_count, friends_itn_count=friends_itn_count, lname=lname, email=email)


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
    # Fetch itinerary_details from the form and store it in db
    if "user" not in session or session["user"] == None:
        return redirect("/")

    user_id = session["user"]["user_id"]
    itn_name = request.args.get("itn_name")
    location = request.args.get("itn_location")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    shareability = request.args.get("shareability")
    notes = request.args.get("notes-ta")
    print(notes)
    friends_emails_ta = request.args.get("friends-email-ta")

    friends_emails = []
    if friends_emails_ta:
        friends_emails = friends_emails_ta.split("\n")

    itn_id = crud.create_itinerary(itn_name, user_id, location, start_date,
                                   end_date, shareability, friends_emails).itinerary_id
    session["itinerary_id"] = itn_id
    session.modified = True

    return redirect("/search")


@app.route("/search")
def search():
    if "user" not in session or session["user"] == None:
        return redirect("/")

    if "itinerary_id" not in session or session["itinerary_id"] == None:
        return redirect("/itinerary-form")

    itn_id = request.args.get("itn_id")
    if not itn_id:
        itn_id = session["itinerary_id"]
    else:
        session["itinerary_id"] = itn_id
        session.modified = True

    itn_name = crud.get_itinerary_details(itn_id)["itn_name"]

    return render_template('search.html', itn_name=itn_name)


@app.route("/load-itinerary")
def load_itinerary():
    """User should be able to load the experience info in experiences and destinations tables."""

    # Fetch exp and destination details from the search display results and store it in db
    exp_name = request.args.get("name")
    reviews = request.args.get("reviews")
    location = request.args.get("location")
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    exp_image = request.args.get("image")
    exp_url = request.args.get("expUrl")
    itn_id = session["itinerary_id"]
    crud.create_experience(exp_name, itn_id, location,
                           latitude, longitude, exp_image, exp_url)

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

    itn_owner = False
    user_id = session["user"]["user_id"]
    itn_id = request.args.get("itn_id")
    itn_info = crud.get_itinerary_details(itn_id)
    itn_user_id = itn_info["user_id"]

    if (itn_user_id == user_id):
        itn_owner = True

    session["itinerary_id"] = itn_id
    session.modified = True

    return render_template('show-itinerary.html', itn_info=itn_info, itn_owner=itn_owner)


@app.route("/get-experiences-filter")
def get_experiences_filter():

    itn_id = session["itinerary_id"]
    experience_state = request.args.get("scheduled_state")
    experience_info = crud.get_experiences(itn_id, experience_state)

    return jsonify(experience_info)

@app.route("/schedule-experience")
def schedule_experience():

    exp_id = request.args.get("exp_id")
    schedule = request.args.get("schedule_date")
    crud.schedule_experience(exp_id, schedule)

    return ""

@app.route("/public-itineraries")
def public_itineraries():
    """Show list of public itineraries."""

    user_id = session["user"]["user_id"]
    public_itns = crud.get_public_itineraries(user_id)

    return render_template('shared-itineraries.html', shared_itns=public_itns)


@app.route("/public-itineraries-list")
def public_itineraries_list():
    """Show list of public itineraries."""

    user_id = session["user"]["user_id"]
    public_itns = crud.get_public_itineraries(user_id)

    return jsonify(public_itns)


@app.route("/get-experiences-carousel")
def get_experiences_carousel():
    """Show list of public itineraries."""

    itn_id = request.args.get("itnId")
    print(itn_id)
    itinerary_info = crud.get_itinerary_details(itn_id)

    return jsonify(itinerary_info)


@app.route("/friends-itineraries")
def friends_itineraries():
    """Show list of friends itineraries."""

    user_id = session["user"]["user_id"]
    friends_itns = crud.get_friends_itineraries(user_id)

    return render_template('shared-itineraries.html', shared_itns=friends_itns)


@app.route("/search-results")
def search_results():
    """Responds to requests made in JS fetch function and returns search results in JSON format."""

    experience = request.args.get("experience")
    location = request.args.get("location")
    results = yelp_api.get_activities(location, experience)
    reviews = yelp_api.get_business_info(location)
    print(json.dumps(reviews))
    return jsonify(results)


@app.route("/delete-itinerary")
def delete_itinerary():
    """Delete itinerary(s)."""
    itn_id = request.args.get("itnId")
    message = crud.delete_itinerary(itn_id)

    return message


@app.route("/delete-experience")
def delete_experience():
    """Delete experience(s)."""
    exp_id = request.args.get("expId")
    message = crud.delete_experience(exp_id)

    return message


@app.route("/edit-itinerary")
def edit_itinerary():
    """Edit user owned itinerary."""

    return "hi"


@app.route("/travel-notes", methods=["POST"])
def travel_notes():
    """Update travel notes"""
    notes = request.json.get("newNotes")
    itn_id = session["itinerary_id"]

    crud.update_notes(itn_id, notes)

    return ""


@app.route("/get-travel-notes")
def get_travel_notes():
    """Get travel notes from the given itn_id"""

    itn_id = session["itinerary_id"]
    notes = crud.get_notes(itn_id)

    return jsonify(notes)


@app.route("/copy-itinerary")
def copy_itinerary():
    """Edit user owned itinerary."""
    user_id = session["user"]["user_id"]
    copy_itn_id = request.args.get("itnId")
    itn_details = crud.get_itinerary_details(copy_itn_id)

    itinerary_name = itn_details["itn_name"]+"_copy"
    location = itn_details["itn_location"]
    start_date = itn_details["start_date"]
    end_date = itn_details["end_date"]
    shareability = 1
    friends_emails = ""
    after_copy_itn_id = crud.create_itinerary(itinerary_name, user_id, location, start_date, end_date, shareability, friends_emails).itinerary_id

    for index in range(len(itn_details["experiences"])):
        exp_name = itn_details["experiences"][index]["exp_name"]
        latitude = itn_details["experiences"][index]["dest_latitude"]
        longitude = itn_details["experiences"][index]["dest_longitude"]
        exp_image = itn_details["experiences"][index]["exp_image"]
        exp_url = itn_details["experiences"][index]["exp_url"]
        crud.create_experience(exp_name, after_copy_itn_id, location,
                            latitude, longitude, exp_image, exp_url)

    itn_info = crud.get_itinerary_details(after_copy_itn_id)
    itn_user_id = itn_info["user_id"]

    if (itn_user_id == user_id):
        itn_owner = True

    session["itinerary_id"] = after_copy_itn_id
    session.modified = True

    return render_template('show-itinerary.html', itn_info=itn_info, itn_owner=itn_owner)
    
    #itn_lst = crud.get_user_itineraries(user_id)
    
    #render_template('show-itinerary.html', )
    #return redirect('view-itineraries')
    #return render_template('view-itineraries.html', itn_lst=itn_lst)


if __name__ == "__main__":
    # connect to db. Else, flask won't be able to access db.
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
