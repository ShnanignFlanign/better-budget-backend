from flask import Flask, jsonify, after_this_request
from flask_login import LoginManager
from dotenv import load_dotenv
import os

#import resource files here later
from resources.accounts import accounts
from resources.transactions import transactions
from resources.deposits import deposits
from resources.users import user

import models 

from flask_cors import CORS 

load_dotenv()

DEBUG = True
PORT = os.getenv("PORT")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

login_manager = LoginManager()

#comment out config for local dev
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='None',
)

CORS(accounts, origins=['https://better-budget.herokuapp.com', 'http://better-budget.herokuapp.com'], supports_credentials=True)
CORS(transactions, origins=['https://better-budget.herokuapp.com', 'http://better-budget.herokuapp.com'], supports_credentials=True)
CORS(deposits, origins=['https://better-budget.herokuapp.com', 'http://better-budget.herokuapp.com'], supports_credentials=True)
CORS(user, origins=['https://better-budget.herokuapp.com', 'http://better-budget.herokuapp.com'], supports_credentials=True)

app.register_blueprint(accounts, url_prefix='/portal/accounts')
app.register_blueprint(transactions, url_prefix='/portal/accounts')
app.register_blueprint(deposits, url_prefix='/portal/accounts')
app.register_blueprint(user, url_prefix='/user')


login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    print("in load user")
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request # use this decorator to cause a function to run before reqs
def before_request():
    """Connect to the db before each request"""
    print("you should see this before each request") # optional -- to illustrate that this code runs before each request -- similar to custom middleware in express.  you could also set it up for specific blueprints only.
    models.DATABASE.connect()
    @after_this_request # use this decorator to Executes a function after this request
    def after_request(response):
        """Close the db connetion after each request"""
        print("you should see this after each request") # optional -- to illustrate that this code runs after each request
        models.DATABASE.close()
        return response # go ahead and send response back to client
                      # (in our case this will be some JSON)

@app.route('/')
def index():
    return 'hi'

if os.environ.get('FLASK_ENV') != 'development':
  print('\non heroku!')
  models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)