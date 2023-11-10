
from flask import Blueprint, request
from ..controllers.authController import test
auth = Blueprint('auth', __name__)

@auth.route("/login")
def login():
    return "<h1>Hi!</h1>"

@auth.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data["name"]
    test(name)
    return "<h1>Success</h1>"
    
    