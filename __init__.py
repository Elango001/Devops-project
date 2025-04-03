from flask import Flask
from database import db
from Config import config
from auth import auth
from views import views
def create_app():
    app = Flask(__name__,template_folder="/home/elango/Documents/projects/flask_web/Devops-project/Templates")
    app.config.from_object(config)
    db.init_app(app)
    app.config['DEBUG'] = True
    app.register_blueprint(auth)
    app.register_blueprint(views)
    return app
