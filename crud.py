"""CRUD operations."""

#import dependencies from model.py file

from model import db, User, Destination, Itinerary, Experience, connect_to_db

#create user function

def create_user(fname, lname, email, password):
    """Create and return a new user."""

    user = create_user(fname=fname, lname=lname, email=email, password=password)

    return user

#create destination function  

def create_destination(destination_name, state, dest_latitude, dest_longitute):
    """Create and return destination info."""

    destination = create_destination(destination_name=destination_name, 
                                     state=state, 
                                     dest_latitude=dest_latitude, 
                                     dest_longitute=dest_longitute)
    
    return destination


#create Itinerary function

def create_itinerary(itinerary_name, destination_id, start_date, end_date):

    itinerary = create_itinerary(itinerary_name=itinerary_name, destination_id=destination_id, 
                                 start_date=start_date, end_date=end_date)

    return itinerary


#create experience function

def create_experience(exp_type, exp_date, itinerary_id, exp_latitude, exp_longitude):

    experience = create_experience(exp_type=exp_type, 
                                   exp_date=exp_date, 
                                   itinerary_id=itinerary_id, 
                                   exp_latitude=exp_latitude, 
                                   exp_longitude=exp_longitude)

    return experience


#To connect to db use the following code

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
