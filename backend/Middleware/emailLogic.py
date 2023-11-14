from flask_mail import Message
from flask import Response, abort, url_for
from flask import Flask, session
from flask_mail import Mail
from ..controllers.authController import confirm_email
import os
from dotenv import load_dotenv
load_dotenv()

WELCOME_TEXT = """Hi! Thanks for joining MusicMania! Verify your email with the link below!"""

#file dedicated to storing all the logic associate with sending an email with flask, all our emails will be the same, its simply for authentication

#helper function to make the message 
def makeMessage(reciever: str, token: str) -> Message:
    confirmEmail = f"http://127.0.0.1:8000/api/auth/confirm/{token}"
    try: 
        msg = Message(
            "MusicMania Account Confirmation",
            recipients=[reciever],
            body = f"Click on the link to activate your email!: {confirmEmail}", 
        )
        return msg
    except Exception:
        abort(Response("Error 401 - Unable To Create Message", status=401))
    