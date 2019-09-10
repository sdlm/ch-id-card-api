from flask import Blueprint, request
from PIL import Image

from .predict.coords import get_card_coords
from .predict.existence import get_card_existence
from .utils import http, image

webapp = Blueprint("webapp", __name__)


@webapp.route("/get_the_same_img", methods=["POST"])
def get_the_same_img():
    img = http.get_image_from_request(request)
    return http.to_response(img)


@webapp.route("/get_square_img", methods=["POST"])
def get_square_img():
    img = http.get_image_from_request(request)
    square_image = image.get_square_image(img)
    return http.to_response(square_image)


@webapp.route("/card_exists", methods=["POST"])
def card_exists():
    img = http.get_image_from_request(request)

    square_img = image.get_square_image(img)

    square_img_128 = square_img.resize((128, 128), Image.ANTIALIAS)

    is_card_exists = get_card_existence(square_img_128)

    return {"card_exists": is_card_exists}


@webapp.route("/get_card", methods=["POST"])
def get_card():
    img = http.get_image_from_request(request)

    square_img = image.get_square_image(img)

    square_img_128 = square_img.resize((128, 128), Image.ANTIALIAS)

    is_card_exists = get_card_existence(square_img_128)

    if not is_card_exists:
        return {"card_exists": is_card_exists}

    square_img_w, _ = square_img.size
    coords = get_card_coords(square_img_128) * (square_img_w / 128)
    card = image.get_card(square_img, coords)

    return http.to_response(card)


@webapp.route("/get_text")
def get_text():
    return {"get_text": "ok"}
