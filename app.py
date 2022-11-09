from flask import Flask
from flask_login import LoginManager

#import resource files here later
from resources.accounts import accounts
from resources.transactions import transactions
from resources.deposits import deposits
from resources.users import user

import models 

from flask_cors import CORS 

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = "superdupersecret"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

CORS(accounts, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(accounts, url_prefix='/portal/accounts')

CORS(transactions, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(transactions, url_prefix='/portal/accounts')

CORS(deposits, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(deposits, url_prefix='/portal/accounts')

CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/user')

@app.route('/')
def index():
    return 'hi'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)