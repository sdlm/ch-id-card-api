from flask import Blueprint

webapp = Blueprint("webapp", __name__)


@webapp.route("/card_exists")
def card_exists():
    return {"card_exists": "ok"}


@webapp.route("/get_card")
def get_card():
    return {"get_card": "ok"}


@webapp.route("/get_text")
def get_text():
    return {"get_text": "ok"}
