
from flask import Blueprint, jsonify, request, abort, Response, session, redirect, url_for, make_response
from ..controllers.authController import registerUser, confirm_email, authorize_user
from ..Middleware.emailLogic import makeMessage

auth = Blueprint('auth', __name__)

#create route to login
@auth.route("/login", methods=["POST"])
def login():

    #check to see if the request is a get first
    if request.method == "POST":
        #get the data from get request
        data = request.get_json()
        #get the userName and password
        identifier = data["identifier"]
        password = data["password"]

        return authorize_user(identifier, password)
    else:
        #someone attempted a non-get request for this
        return make_response(jsonify({'error': 'Unauthroized Access'}), 200)
    
#create signup route
@auth.route("/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        #get the data from the request
        data = request.get_json()
        #get all the data from the fields
        firstName = data["first-name"]
        lastName = data["last-name"]
        userName = data["user-name"]
        email = data["email"]
        password = data["password"]
        confirmPassword = data["confirm-password"]

        #use registerUser in the controllers to register the user to the db
        return registerUser(firstName, lastName, userName, email, password, confirmPassword)

    else:
        #someone attempted a non-post request
        return make_response(jsonify({'error': 'Unauthroized Access'}), 200)

@auth.route("/make-email", methods=["POST"])
def makeEmail():
    if request.method == "POST":
        #create the url for sending the mail
        email_url = url_for("sendMail", token = session['userInfo'])
        #send the redirect to the mail
        return redirect(email_url)   

#route to confirm the user once they verify their email
@auth.route("/confirm/<token>", methods = ["PUT"])
def confirmUser(token):
    #check to see if the method was PUT
    if request.method == "PUT":
        #check to see if the correct user is trying to authenticate their account
        if session['userInfo'] == token:
            try:
                #confirm the email address is valid
                return confirm_email(session['userInfo'])
                #tell the user the resposne went good!
            except Exception:
                return make_response(jsonify({'error': 'Unable to authorize email'}), 200)
        else:
            print("HEY")
            return make_response(jsonify({'error': 'Must be Signed In To Confirm Email'}), 400)
    else:
        return make_response(jsonify({'error': 'Unauthroized Access'}), 400)
    
    