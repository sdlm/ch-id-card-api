from flask import Flask, jsonify

from . import settings
from .exceptions import InvalidUsage
from .handlers import webapp

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = settings.UPLOAD_FOLDER
app.secret_key = "super secret key"
app.register_blueprint(webapp)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def ping():
    return {"status": "ok"}
