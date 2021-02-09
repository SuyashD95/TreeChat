from flask import Flask
from flask_restful import Api
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
class User(db.Model):
    """Model class defined for the User table."""

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.relationship('Room', backref='user', lazy=True)
    sends = db.relationship('Message', backref='user', lazy=True)

    def __repr__(self):
        """Object representation for a record of User."""
        return f'User(name={self.name}, email={self.email}, password={self.password})'


class Room(db.Model):
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


if __name__ == '__main__':
    app.run(debug=True)
