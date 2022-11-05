from flask import Flask
from flask_login import LoginManager

#import resource files here later

#import models here once set up

from flask_cors import CORS 

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = "superdupersecret"

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def index():
    return 'hi'

if __name__ == '__main__':
    #models.initialize()
    app.run(debug=DEBUG, port=PORT)