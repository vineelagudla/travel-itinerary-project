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

def create_destination(destination_name, dest_latitude, dest_longitude):
    """Create and return destination info."""

    destination = Destination(destination_name = destination_name, dest_latitude= dest_latitude, dest_longitude = dest_longitude)
    
    db.session.add(destination)
    db.session.commit()

    return destination


#create Itinerary function

def create_itinerary(itinerary_name, user_id, location, start_date, end_date):

    itinerary = Itinerary(itinerary_name=itinerary_name, user_id=user_id, 
                                location=location, 
                                start_date=start_date, end_date=end_date)

    db.session.add(itinerary)
    db.session.commit()

    return itinerary


def get_itinerary_details(itn_id):

    itinerary = Itinerary.query.get(itn_id)
    itinerary_info = {}

    itinerary_info["itn_name"] = itinerary.itinerary_name
    itinerary_info["itn_location"] = itinerary.location
    itinerary_info["start_date"] = itinerary.start_date
    itinerary_info["end_date"] = itinerary.end_date
    itinerary_info["experiences"] = []

    experiences = Experience.query.filter(Experience.itinerary_id == itn_id).all()
    for experience in experiences:
        experience_info = {}
        experience_info["exp_id"] = experience.exp_id
        experience_info["exp_name"] = experience.exp_name
        destination = Destination.query.get(experience.dest_id)
        experience_info["dest_name"] = destination.destination_name
        experience_info["dest_latitude"] = destination.dest_latitude
        experience_info["dest_longitude"] = destination.dest_longitude

        itinerary_info["experiences"].append(experience_info)

    return itinerary_info


def get_user_itineraries(user_id):

    user_itineraries = Itinerary.query.filter(Itinerary.user_id == user_id)

    user_itineraries_lst = []

    for user_itinerary in user_itineraries:
        user_itinerary_info = {}

        user_itinerary_info["itn_name"] = user_itinerary.itinerary_name

        user_itinerary_info["itn_id"] = user_itinerary.itinerary_id

        user_itineraries_lst.append(user_itinerary_info)
    
    return user_itineraries_lst


#create experience function

def create_experience(exp_name, itinerary_id, location, exp_latitude, exp_longitude):

    destination = create_destination(location, exp_latitude, exp_longitude)

    experience = Experience(exp_name=exp_name, itinerary_id=itinerary_id, dest_id= destination.destination_id)

    db.session.add(experience)
    db.session.commit()

    return experience


def get_experience_details(itn_id):

    experience = Experience.query.get(itn_id)
    destination = Destination.query.get(0)
    experience_info = {}
    experience_info["exp_name"] = experience.exp_name

    return experience_info

#To connect to db use the following code

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
