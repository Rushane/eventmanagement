from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app)

app.config.from_pyfile('config.py')
db= SQLAlchemy(app)


from views import *

if __name__ == '__main__':
    app.run(debug=True)
