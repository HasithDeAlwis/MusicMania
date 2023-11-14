from ..database import connection, CREATE_USER_TABLE, INSERT_USER, FIND_TOKEN, VERIFY_EMAIL, FIND_SAME_EMAIL
from ..tokens import encode_user
import bcrypt
from flask import flash, session, abort, Response
from ..tokens import decode_user

DROP_TABLE = "DROP TABLE users"


def registerUser(firstName: str, lastName: str, userName: str, email: str, password: str, confirmPassword: str):
    print(email)
    token = encode_user(email)
    
    if (not firstName or not lastName or not userName or not email or not password or not confirmPassword):
        abort(Response("Please enter all fields", status=400, content_type='text/plain'))
    
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(FIND_SAME_EMAIL, (email,))
                account = cursor.fetchone()
    except Exception:
        abort(Response("Could not not process request", status=401, content_type="text/plain"))
        
    if (account):
        abort(Response("Account already exists", status=400, content_type='text/plain'))
    
    if (password == confirmPassword):
        hashedPassword = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())        
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_USER_TABLE)
                cursor.execute(INSERT_USER, (firstName, lastName, userName, email, hashedPassword, token,))
        session['userInfo'] = token   
    else:
        abort(Response("Passwords do not match", status=400, content_type='text/plain'))
    

#helper function to confirm the email of a user
def confirm_email(token: str):
    #get the account associate with the token 
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(FIND_TOKEN, (token,))
            #get the account info
            account = cursor.fetchone()
    
    #if the result at the 7th index, the confirmed status is true, then do nothing
    if account[7] == True:
        flash("Account already confirmed.", "success")
        return "<h1>Success</h1>"
    
    
    try:    
        #check to see if the session is empty or not
        if (session['userInfo']):
            #verify whether it is the correct user accessing the API endpoint
            if token == session['userInfo']:
                #start db connection
                with connection:
                    with connection.cursor() as cursor:
                        #update the user to have isConfirmed
                        cursor.execute(VERIFY_EMAIL, (token,))

                flash("You have confirmed your account. Thanks!", "success")
            else:
                flash("The confirmation link is invalid or has expired.", "danger")
        else:
            abort(400, Response("Must Login First"))
    except Exception:
        abort(401, Response("Server Error"))
    

    