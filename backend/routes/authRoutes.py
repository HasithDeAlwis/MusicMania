
from flask import Blueprint, request, abort, Response, session, redirect, url_for
from ..controllers.authController import registerUser, confirm_email
from ..Middleware.emailLogic import makeMessage

auth = Blueprint('auth', __name__)

@auth.route("/login")
def login():
    return "<h1>Hi!</h1>"

@auth.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    firstName = data["first-name"]
    lastName = data["last-name"]
    userName = data["user-name"]
    email = data["email"]
    password = data["password"]
    confirmPassword = data["confirm-password"]
    
    registerUser(firstName, lastName, userName, email, password, confirmPassword)
    
    email_url = url_for("sendMail", token = session['userInfo'])
    
    return redirect(email_url)
    
@auth.route("/confirm/<token>", methods = ["PUT"])
def confirmUser(token):
    if session['userInfo'] == token:
        if request.method == "PUT":
            try:
                confirm_email(session['userInfo'])
            except Exception:
                abort(Response("Error 401 - Unable to Authorize Email", status=401))
    else:
        abort(Response("Error - Email expired or invalid entry ", status=401))
    return Response("Email Confirmed!", status=200)
    
    