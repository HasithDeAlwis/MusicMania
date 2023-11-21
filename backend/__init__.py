from flask import Flask, jsonify, make_response, session, Response
from flask_mail import Mail
import os
from dotenv import load_dotenv
from .Middleware.emailLogic import makeMessage
from .tokens import decode_user
from flask_cors import CORS
import requests

load_dotenv()
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")


#import blueprints
from .routes.authRoutes import auth
from .routes.spotifyRoutes import spotify
    
    
#set up flask app
app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

    
#arbritary secrete key 
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
    
    
    #setting up the mail config for the appp
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("NEW_MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

#create mail variable which will send the emails
mail = Mail(app)

#****register all the routes needed for our backend*****
#regist the routes fo the authentication
app.register_blueprint(auth, url_prefix="/api/auth")

#register the routes for spotify API
app.register_blueprint(spotify, url_prefix="/api/spotify")

@app.route("/api/email/<token>")
def sendMail(token):
    if token == session['userInfo']:
        email = decode_user(token)
        msg = makeMessage(email['email'], session['userInfo'])
        print(msg.recipients, msg.sender)
        mail.send(msg)
    return make_response(jsonify({'message': 'Registered! Confirmation Email Sent'}), 200)
