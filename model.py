
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User related information."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    #creating relationship with User and Itinerary tables

    itineraries = db.relationship("Itinerary", back_populates="user")

    def __repr__(self):
        #Show user information

        return f'<User user_id = {self.user_id} email = {self.email}>'


class Destination(db.Model):
    """Destination related information."""

    __tablename__ = 'destinations'

    destination_id = db.Column(db.Integer,
                               autoincrement=True,
                               primary_key=True)
    destination_name = db.Column(db.String)
    dest_latitude = db.Column(db.Float)
    dest_longitude = db.Column(db.Float)

    #creating relationship between Destinations and Itinerary tables

    experiences  = db.relationship("Experience", back_populates="destination")

    def __repr__(self):
        #Show destination info

        return f'<Destination destination_id = {self.destination_id} destination_name = {self.destination_name}>'

class Itinerary(db.Model):

    """Itinerary details."""

    __tablename__ = 'itineraries'

    itinerary_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    itinerary_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    location = db.Column(db.String)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    share_to_public = db.Column(db.String)

    #create a relationship between User, Destination and Experience tables

    user = db.relationship("User", back_populates="itineraries")
    experiences = db.relationship("Experience", back_populates="itinerary")

    def __repr__(self):
        #Show itinerary information

        return f'<Itinerary itinerary_id = {self.itinerary_id} itinerary_name = {self.itinerary_name}>' 

class Experience(db.Model):
    """EXperience information."""   

    __tablename__ = 'experiences'

    exp_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    exp_name = db.Column(db.String)
    exp_type = db.Column(db.String)
    
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.itinerary_id'))
    dest_id  = db.Column(db.Integer, db.ForeignKey('destinations.destination_id'))

    #creating relationship between Destinations and Itinerary tables

    itinerary  = db.relationship("Itinerary", back_populates="experiences")
    destination  = db.relationship("Destination", back_populates="experiences")

    def __repr__(self):
        #Show experience information

        return f'<Experience exp_id = {self.exp_id} exp_type = {self.exp_type}>' 


def connect_to_db(flask_app, db_uri="postgresql:///itineraries", echo=False):
    
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)                          

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)


# def connect_to_db(app, itineraries):
#     """Connect to database."""

#     app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///itineraries"
#     app.config["SQLALCHEMY_ECHO"] = True
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#     db.app = app
#     db.init_app(app)   