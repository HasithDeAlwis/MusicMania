#Importing createApp() method in the __init__.py file that will run each time the app is run
from backend import app

#start the host on port8000
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)