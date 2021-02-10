from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

# App Configuration
# -----------------
app = Flask(__name__)
api = Api(app)
# Local SQLite3 Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# -----------------

# Local Database Models
# ---------------------
class UserModel(db.Model):
    """Model class defined for the User table."""

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(256), nullable=True)
    is_admin = db.relationship('Room', backref='user', lazy=True)
    sends = db.relationship('Message', backref='user', lazy=True)

    def __repr__(self):
        """Object representation for a record of User."""
        return f'User(name={self.name}, email={self.email}, password={self.password})'


class RoomModel(db.Model):
    """Model class defined for the Room table."""

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    admin_id = db.Column(db.Integer, 
        db.ForeignKey('user._id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    messages = db.relationship('Message', backref='room', lazy=True)

    def __repr__(self):
        """Object representation for a record of a Room."""
        return f'Room(name={self.name}, admin={self.user.name})'


class MessageModel(db.Model):
    """Model class defined for the Message table."""

    _id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    sender_id = db.Column(db.Integer,
        db.ForeignKey('user._id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False    
    )
    room_id = db.Column(db.Integer,
        db.ForeignKey('room._id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )

    def __repr__(self):
        """Object representation for a record of a Message."""
        return f'Message(body={self.text}, timestamp={self.timestamp}, sender={self.user.name}, room={self.room.name}'
# ---------------------


# Request Parsers
# ---------------
# Add the request parser to verify that the user has passed in the
# necessary fields in the JSON object to successfully create a new user.
user_post_reqparser = reqparse.RequestParser()
user_post_reqparser.add_argument('name', type=str, help='Username is a mandatory field.', required=True)
user_post_reqparser.add_argument('password', type=str, help='Password is a mandatory field.', required=True)
user_post_reqparser.add_argument('email', type=str, help='Email is an optional field.')

# Add the request parser to verify that the user has passed in the
# necessary fields in the JSON object to successfully create a new room.
room_post_reqparser = reqparse.RequestParser()
room_post_reqparser.add_argument('name', type=str, 
    help='Required. Name of the Room.', required=True
)
room_post_reqparser.add_argument('room_admin_name', type=str,
    help='Required. Name of the user who is the admin of the room.', required=True
)

# Add the request parser to verify that the user has passed in the
# necessary fields in the JSON object to successfully create a new message.
message_post_reqparser = reqparse.RequestParser()
message_post_reqparser.add_argument('body', type=str, 
    help='Required. Body of the message. Cannot be empty.', required=True
)
message_post_reqparser.add_argument('timestamp', type=str,
    help='Required. Timestamp for the message expressed as a string.', required=True
)
message_post_reqparser.add_argument('sender_name', type=str, 
    help='Required. Name of the sender.', required=True
)
message_post_reqparser.add('room_name', type=str, 
    help='Required. Name of the room.', required=True
)


# API Resources
# -------------
class UserEntity(Resource):
    """Resource class to handle requests made to the 'users' table 
    in the database at the specified endpoints:
        1. /users/all
        2. /users/new
    
    Handles the following requests along with a summary:
        1. GET  - Get all the users.
        2. POST - Create a new user.
    """

    def get():
        """Handles GET requests for the resource and return HTTP code 200
        on a successful completion of a request.

        Return a JSON response back to the user containing details
        about all the users stored in the database.
        
        Abort handling GET requests and return 404 if no users exist
        in the database along with an error message.
        """
        pass

    def post():
        """Handles POST requests at the specified endpoint and returns status
        code 201 representing that a new user has been inserted into the
        database along with a JSON response containing information about
        the newly created user.

        Also, if the necesasary data required to insert a new user is not provided,
        return a 400 error, along with some information about the problem with the given
        data as an error message.
        
        Aborts the request if a member with the passed name already exists
        and thus, return a 409 error code with an error message.
        """
        pass


class UserRecord(Resource):
    """Resource class to handle requests made to a specific record
    of the 'users' table of the database at the specified endpoint(s): 
        1. /users/{name}
    
    Handles the following request(s) along with a summary::
        1. GET - Get a user by their name.
    """

    def get(name):
        """Handles GET requests at the specified endpoint and return
        HTTP code 200 on a successful completion of a request.
        
        The parameter name should be identical to the name of the user that
        could potentially exist in the database. This means that "Name"
        and "NaMe" are treated as two different values because their cases
        are different, even though they mean the same.
        
        Return a JSON response containing details about the specified user.

        Abort handling GET requests and return 404 if no user with
        the specified name is found along with an error message.
        """
        pass


class RoomEntity(Resource):
    """Resource class to handle requests made to the 'rooms' table 
    in the database at the specified endpoints:
        1. /rooms/all
        2. /rooms/new
    
    Handles the following requests along with a summary:
        1. GET  - Get all the rooms.
        2. POST - Create a new room.
    """

    def get():
        """Handles GET requests at the endpoint and return HTTP code 200
        on a successful completion of a request.

        Return a JSON response back to the user containing details
        about all the rooms stored in the database.
        
        Abort handling GET requests and return 404 if no rooms exist
        in the database along with an error message.
        """
        pass

    def post():
        """Handles POST requests at the specified endpoint and returns status
        code 201 representing that a new room has been inserted into the
        database along with a JSON response containing information about
        the newly created room.

        Also, if the necesasary data required to insert a new room is not provided,
        return a 400 error, along with some information about the problem with the given
        data as an error message.
        
        Aborts the request if a room with the passed name already exists
        and thus, return a 409 error code with an error message.
        """
        pass


class RoomRecord(Resource):
    """Resource class to handle requests made to a specific record
    of the 'rooms' table of the database at the specified endpoint(s): 
        1. /rooms/{name}
    
    Handles the following request(s) along with a summary::
        1. GET - Get a room by their name.
    """

    def get(name):
        """Handles GET requests at the specified endpoint and return
        HTTP code 200 on a successful completion of a request.
        
        The parameter name should be identical to the name of the room that
        could potentially exist in the database. This means that "Room"
        and "RooM" are treated as two different values because their cases
        are different, even though they mean the same.
        
        Return a JSON response containing details about the specified room.

        Abort handling GET requests and return 404 if no room with
        the specified name is found along with an error message.
        """
        pass


class Message(Resource):
    """Resource class to handle requests made to the 'messages' table 
    in the database at the specified endpoints:
        1. /messages/{room_name}
        2. /messages/new
    
    Handles the following requests along with a summary:
        1. GET  - Get all the messages of a particular room.
        2. POST - Create a new message.
    """

    def get(room_name):
        """Handles GET requests at the endpoint and return HTTP code 200
        on a successful completion of a request.

        The parameter room_name should be identical to the name of the room that
        could potentially exist in the database. This means that "Room"
        and "RooM" are treated as two different values because their cases
        are different, even though they mean the same.
        
        Return a JSON response back to the user containing details
        about all the messages that were passed between members of the
        given room.
        
        Abort handling GET requests with an 404 error code along with
        an error message if:\n
            1. The room specified by room_name parameter doesn't exist, or;\n
            2. No messages exist for a given room in the database.
        """
        pass

    def post():
        """Handles POST requests at the specified endpoint and returns status
        code 201 representing that a new message has been inserted into the
        database along with a JSON response containing information about
        the newly created message.

        Also, if the necesasary data required to insert a new nessage is not provided,
        return a 400 error, along with some information about the problem with the given
        data as an error message.
        
        Aborts the request if a message with no content i.e., empty body is sent
        to the server and thus, return a 409 error code with an error message.
        """
        pass  
# -------------


# Register Resources to API Endpoints 
# -----------------------------------
api.add_resource(UserEntity, '/users/new', endpoint='create_new_user')
api.add_resource(UserEntity, '/users/all', endpoint='get_all_users')
api.add_resource(UserRecord, '/users/<string:name>', endpoint='get_user_by_name')
api.add_resource(RoomEntity, '/rooms/new', endpoint='create_new_room')
api.add_resource(RoomEntity, '/rooms/all', endpoint='get_all_rooms')
api.add_resource(RoomRecord, '/rooms/<string:name>', endpoint='get_room_by_name')
api.add_resource(Message, '/messages/new', endpoint='create_new_message')
api.add_resource(Message, '/messages/<string:room_name>', endpoint='get_all_msgs_of_a_room')
# -----------------------------------

if __name__ == '__main__':
    app.run(debug=True)
