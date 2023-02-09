"""CRUD operations."""

#import dependencies from model.py file
from model import db, User, Destination, Itinerary, Experience, ItinerariesFriends, connect_to_db
from datetime import date

#create user function
def create_user(fname, lname, email, password):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(user)
    db.session.commit()

#Gets user information from db and returns in the form of dictionary
def get_user_details(email):

    user = User.query.filter(User.email == email).first()
    user_info = {}
    if user:
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
def create_itinerary(itinerary_name, user_id, location, start_date, end_date, shareability, friends_emails):

    itinerary = Itinerary(itinerary_name=itinerary_name, user_id=user_id, 
                                location=location, 
                                start_date=start_date, end_date=end_date, shareability=shareability)

    db.session.add(itinerary)
    db.session.commit()

    if shareability == "2":
        itn_id = itinerary.itinerary_id
        create_itineraries_friends(itn_id, friends_emails)

    return itinerary
#create associative table between users and itineraries table
def create_itineraries_friends(itn_id, friends_emails):
    for friend_email in friends_emails:
        friend_email = friend_email.strip()
        friend = User.query.filter(User.email == friend_email).first()
        if friend:
            itineraries_friends = ItinerariesFriends(itinerary_id=itn_id, user_id=friend.user_id)

            db.session.add(itineraries_friends)
            db.session.commit()


#Gets itinerary information from db to display the details of the selected itinerary 
def get_itinerary_details(itn_id):

    itinerary = Itinerary.query.get(itn_id)

    itinerary_info = {}

    itinerary_info["itn_id"] = itinerary.itinerary_id
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
        experience_info["exp_image"] = experience.exp_image
        experience_info["exp_url"] = experience.exp_url
        destination = Destination.query.get(experience.dest_id)
        experience_info["dest_name"] = destination.destination_name
        experience_info["dest_latitude"] = destination.dest_latitude
        experience_info["dest_longitude"] = destination.dest_longitude

        itinerary_info["experiences"].append(experience_info)

    return itinerary_info

#Gets user owned itinerary information from db
def get_user_itineraries(user_id):
    #Returns list of itinerary objects associated for the given user.
    user_itineraries = Itinerary.query.filter(Itinerary.user_id == user_id).all()

    user_owned_itineraries = []

    for user_itinerary in user_itineraries:
        user_itinerary_info = {}

        user_itinerary_info["itn_name"] = user_itinerary.itinerary_name

        user_itinerary_info["itn_id"] = user_itinerary.itinerary_id

        user_owned_itineraries.append(user_itinerary_info)
    
    return user_owned_itineraries

#Returning itinerary count to enable/disbale owned itinerary button in itinerary page
def get_itinerary_count(user_id):

    shared_itineraries = Itinerary.query.filter(Itinerary.user_id == user_id).all()

    return len(shared_itineraries)

def get_friends_itineraries(user_id):
    itineraries_friends = ItinerariesFriends.query.filter(ItinerariesFriends.user_id == user_id).all()

    itn_ids = []
    for itinerary_friend in itineraries_friends:
        itn_ids.append(itinerary_friend.itinerary_id)
    
    friends_itineraries_lst = []
    for itn_id in itn_ids:
        friends_itinerary_info = {}
        friends_itinerary_info["itn_id"] = itn_id
        itn_name = Itinerary.query.get(itn_id).itinerary_name
        friends_itinerary_info["itn_name"] = itn_name
        friends_itineraries_lst.append(friends_itinerary_info)

    return friends_itineraries_lst

#Returning itinerary count to enable/disbale friends itinerary button in itinerary page
def get_friends_itinerary_count(user_id):
    itineraries_friends = ItinerariesFriends.query.filter(ItinerariesFriends.user_id == user_id).all()

    return len(itineraries_friends)

#Gets publicly shared itinerary details
def get_public_itineraries(user_id):
    public_itineraries = Itinerary.query.filter(Itinerary.user_id != user_id, Itinerary.shareability == 3).all()

    public_itineraries_lst = []

    for public_itinerary in public_itineraries:
        public_itinerary_info = {}

        public_itinerary_info["itn_name"] = public_itinerary.itinerary_name

        public_itinerary_info["itn_id"] = public_itinerary.itinerary_id

        public_itineraries_lst.append(public_itinerary_info)

    return public_itineraries_lst

#Returning itinerary count to enable/disbale public itinerary button in itinerary page
def get_public_itinerary_count(user_id):
    public_itineraries = Itinerary.query.filter(Itinerary.user_id != user_id, Itinerary.shareability == 3).all()

    return len(public_itineraries)


#Delete itinerary
def delete_itinerary(itn_id):

    delete_itinerary = Itinerary.query.get(itn_id)

    delete_itinerary_exp_lst = Experience.query.filter(Experience.itinerary_id == itn_id).all()

    for delete_exp in delete_itinerary_exp_lst:
        db.session.delete(delete_exp)
        db.session.commit()
        
    db.session.delete(delete_itinerary)
    db.session.commit()

    return "Deleted"

#create experience function
def create_experience(exp_name, itinerary_id, location, exp_latitude, exp_longitude, exp_image, exp_url):

    destination = create_destination(location, exp_latitude, exp_longitude)

    experience = Experience(exp_name=exp_name, itinerary_id=itinerary_id, dest_id= destination.destination_id, exp_image=exp_image, exp_url=exp_url)

    db.session.add(experience)
    db.session.commit()

    return experience


def delete_experience(exp_id):

    delete_itinerary = Experience.query.get(exp_id)

    delete_itinerary_exp_lst = Experience.query.filter(Experience.exp_id == exp_id).all()

    for delete_exp in delete_itinerary_exp_lst:
        db.session.delete(delete_exp)
        db.session.commit()

    return "Experience Deleted"

    
#To connect to db use the following code
if __name__ == '__main__':
    from server import app
    connect_to_db(app)
