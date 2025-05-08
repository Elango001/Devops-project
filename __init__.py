from flask import Flask
from database import db
from Config import config
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")  # define it at the top level

def create_app():
    app = Flask(__name__, template_folder="/home/elango/Documents/projects/flask_web/Devops-project/Templates")
    app.config.from_object(config)
    db.init_app(app)
    app.config['DEBUG'] = True 
    from auth import auth
    from views import views
    from nothing import nothing
    app.register_blueprint(auth)
    app.register_blueprint(nothing)
    app.register_blueprint(views)
    socketio.init_app(app)  # initialize it here
    return app
