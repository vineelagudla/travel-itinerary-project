"""CRUD operations."""

#import dependencies from model.py file

from model import db, User, Destination, Itinerary, Experience, connect_to_db
from datetime import date

#create user function

def create_user(fname, lname, email, password):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(user)
    db.session.commit()


def get_user_details(email):

    user = User.query.filter(User.email == email).first()
    user_info = {}
    user_info["user_id"] = user.user_id
    user_info["fname"] = user.fname
    user_info["lname"] = user.lname
    user_info["email"] = user.email
    user_info["password"] = user.password

    return user_info


#create Destination function  

def create_destination(destination_name, dest_latitude, dest_longitute):
    """Create and return destination info."""

    destination = Destination(destination_name=destination_name, 
                                     dest_latitude=dest_latitude, 
                                     dest_longitute=dest_longitute)
    
    return destination


#create Itinerary function

def create_itinerary(itinerary_name, user_id, location, start_date, end_date):

    itinerary = Itinerary(itinerary_name=itinerary_name, user_id=user_id, 
                                location=location, 
                                start_date=start_date, end_date=end_date)

    db.session.add(itinerary)
    db.session.commit()

    return itinerary

#get itinerary details
def get_itinerary_details(itn_id):

    itinerary = Itinerary.query.get(itn_id)
    itinerary_info = {}

    itinerary_info["itn_name"] = itinerary.itinerary_name
    itinerary_info["itn_location"] = itinerary.location
    itinerary_info["start_date"] = itinerary.start_date
    itinerary_info["end_date"] = itinerary.end_date

    return itinerary_info


#create experience function

def create_experience(exp_name, exp_type, itinerary_id, exp_latitude, exp_longitude):

    experience = Experience(exp_name=exp_name,exp_type=exp_type)

    db.session.add(experience)
    db.session.commit()

    return experience


#To connect to db use the following code

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
