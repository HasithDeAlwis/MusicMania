from ..database import connection, CREATE_USER_TABLE, INSERT_USER, FIND_TOKEN, VERIFY_EMAIL, FIND_SAME_ACCOUNT
from ..tokens import encode_user
import bcrypt
from flask import flash, session, abort, Response
from ..tokens import decode_user

DROP_TABLE = "DROP TABLE users"

#a funciton to register the user into the database and site
def registerUser(firstName: str, lastName: str, userName: str, email: str, password: str, confirmPassword: str):
    #create a special token for the user based on their id
    token = encode_user(email)
    
    #if any fields are not entered then abort with a 400 error
    if (not firstName or not lastName or not userName or not email or not password or not confirmPassword):
        abort(Response("Please enter all fields", status=400, content_type='text/plain'))
    
    #check the database to see if anyone has the same email
    try:
        with connection:
            with connection.cursor() as cursor:
                #find someone with the same eamil
                cursor.execute(FIND_SAME_ACCOUNT, (email, userName,))
                account = cursor.fetchone()
    except Exception:
        #error with db query
        abort(Response("Server Error", status=401, content_type="text/plain"))

    #if accounts is not empty then abort with 400 error
    if (account):
        abort(Response("Account already exists", status=400, content_type='text/plain'))
    
    #check to see if passwords match
    if (password == confirmPassword):
        #hash password
        hashedPassword = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()) 
        with connection:
            with connection.cursor() as cursor:
                hashedPassword = hashedPassword.decode('utf-8')
                #make the user table if it doesnt exist
                cursor.execute(CREATE_USER_TABLE)
                #insert the new user into the table
                cursor.execute(INSERT_USER, (firstName, lastName, userName, email, hashedPassword, token,))
        #save the user token in the dbs
        session['userInfo'] = token   
    else:
        abort(Response("Passwords do not match", status=400, content_type='text/plain'))

#authorize the user to login
def authorize_user(identifier: str, password: str) -> Response:
    #query the db for someone with the same account as the identifier provided, it can be an email or username
    try:
        with connection:
            with connection.cursor() as cursor:
                #find someone with the same eamil
                cursor.execute(FIND_SAME_ACCOUNT, (identifier, identifier,))
                #fetch the one account
                account = cursor.fetchone()
    except:
        abort(Response("Server Error", status=400))
    
    #if the account exist then check to see if hte passwords of that account match
    if (account):
        if bcrypt.checkpw(password.encode('utf8'), account[5].encode('utf8')):
            #set the userInfo to be the session
            session['userInfo'] = account[6]
            return Response("Successfuly Logged In!")
        else:
            #password is not the same
            abort(Response("Password or Username Does Not Match", status=401, content_type='text/plain')) 
    else:
        #account does not exist
        abort(Response("Password or Username Does Not Match", status=401, content_type='text/plain'))

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
            else:
                #abort the program
                abort(Response("Link has expired or is invalid", status=401, content_type='text/plain'))
        else:
            #the user is not logged in and trying to verify their email
            abort(Response("Must Login First", status=400))
    except Exception:
        #Error with connecting to the database
        abort(Response("Server Error", status=401))


    

    