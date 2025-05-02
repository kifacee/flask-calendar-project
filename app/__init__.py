from app import routes      #from 'app' folder import 'routes.py'
from app.config import Config
from flask import Flask

app = Flask(__name__)

app.config.from_object(Config)
print("SECRET KEY IS: ", app.config["SECRET_KEY"])
# alternative if not using a Config class
# app.config.update({'SECRET_KEY': os.environ.get('SECRET_KEY')}) #update the config dictionary with the secret key env variable

app.register_blueprint(routes.bp)       #register the 'main' blueprint


# User name	calendar_this
# Database name	calendar_this_dev
# Password	Ku9rSyXD
