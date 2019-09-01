from flask import Flask

from . import settings
from .handlers import webapp

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = settings.UPLOAD_FOLDER
app.secret_key = "super secret key"
app.register_blueprint(webapp)


@app.route("/")
def ping():
    return {"status": "ok"}
