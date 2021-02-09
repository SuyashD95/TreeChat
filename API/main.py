from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

# App Configuration
app = Flask(__name__)
api = Api(app)
# Local SQLite3 Database Configuration
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///test_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# -----------------

# Database Models
# ---------------


if __name__ == '__main__':
    app.run(debug=True)
