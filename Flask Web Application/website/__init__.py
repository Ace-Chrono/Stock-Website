from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'uhgowihgoiwhrgpqdfknvsllvksn'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/') #Defines the url prefix that the route has to go through
    app.register_blueprint(auth, url_prefix='/') #If the prefix was /auth/ and auth.route("hello") to access thr route you would have to go to /auth/hello

    return app
