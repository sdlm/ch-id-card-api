from flask import Blueprint

webapp = Blueprint("webapp", __name__)


@webapp.route("/get_the_same_img")
def get_the_same_img():
    return {"get_the_same_img": "ok"}


@webapp.route("/get_square_img")
def get_square_img():
    return {"get_square_img": "ok"}


@webapp.route("/card_exists")
def card_exists():
    return {"card_exists": "ok"}


@webapp.route("/get_card")
def get_card():
    return {"get_card": "ok"}


@webapp.route("/get_text")
def get_text():
    return {"get_text": "ok"}
