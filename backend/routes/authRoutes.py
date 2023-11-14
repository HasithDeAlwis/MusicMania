
from flask import Blueprint, request, abort, Response, session, redirect, url_for
from ..controllers.authController import registerUser, confirm_email, authorize_user
from ..Middleware.emailLogic import makeMessage

auth = Blueprint('auth', __name__)

#create route to login
@auth.route("/login", methods=["GET"])
def login():
    #check to see if the request is a get first
    if request.method == "GET":
        #get the data from get request
        data = request.get_json()
        #get the userName and password
        identifier = data["identifier"]
        password = data["password"]
        return authorize_user(identifier, password)
    else:
        #someone attempted a non-get request for this
        abort(Response("Unauthroized access", status=403))
    
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
        registerUser(firstName, lastName, userName, email, password, confirmPassword)
        #create the url for sending the mail
        email_url = url_for("sendMail", token = session['userInfo'])
        #send the redirect to the mail
        return redirect(email_url)
    else:
        #someone attempted a non-post request
        abort(Response("Anauthorized access", status=403))

#route to confirm the user once they verify their email
@auth.route("/confirm/<token>", methods = ["PUT"])
def confirmUser(token):
    #check to see if the method was PUT
    if request.method == "PUT":
        #check to see if the correct user is trying to authenticate their account
        if session['userInfo'] == token:
            try:
                #confirm the email address is valid
                confirm_email(session['userInfo'])
                #tell the user the resposne went good!
                return Response("Email Confirmed!", status=200)
            except Exception:
                abort(Response("Error 401 - Unable to Authorize Email", status=401))
    else:
        abort(Response("Error - Email expired or invalid entry ", status=401))
    
    