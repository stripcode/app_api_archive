import logging
from logging.handlers import TimedRotatingFileHandler
from flask import Flask
from flask_cors import CORS
from domain import db
from privateApi import app as privateApi
from publicApi import app as publicApi



app = Flask(__name__)
CORS(app)
app.config.from_object("config")
db.init_app(app)
app.register_blueprint(privateApi, url_prefix = "/api/private")
app.register_blueprint(publicApi, url_prefix = "/api/public")



if not app.debug:
  app.logger.setLevel(logging.INFO)
  handler = TimedRotatingFileHandler(app.config["LOG_FILE"], when = "D")
  handler.setLevel(logging.INFO)
  formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s')
  handler.setFormatter(formatter)
  app.logger.addHandler(handler)

if __name__ == "__main__":
  app.run(debug = True, host = app.config["HOST"], port = app.config["PORT"])