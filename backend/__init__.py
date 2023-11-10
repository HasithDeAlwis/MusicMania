from flask import Flask

def createApp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "ascw2dfa-2341234"
    
    from .routes.authRoutes import auth
     
    app.register_blueprint(auth, url_prefix="/api/")
    
    return app

