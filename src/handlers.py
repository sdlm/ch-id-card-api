from flask import Blueprint, request, send_file
from PIL import Image

from .predict.existence import get_card_existence
from .utils import http, image

webapp = Blueprint("webapp", __name__)


@webapp.route("/get_the_same_img", methods=["POST"])
def get_the_same_img():
    img = http.get_image_from_request(request)

    print(f"Received img.size: {img.size}, mode: {img.mode}")

    out_img = img

    return send_file(
        http.prepare_file_to_output(out_img),
        attachment_filename="mask.jpg",
        mimetype="image/jpg",
    )


@webapp.route("/get_square_img", methods=["POST"])
def get_square_img():
    img = http.get_image_from_request(request)

    out_img = image.get_square_image(img)

    return send_file(
        http.prepare_file_to_output(out_img),
        attachment_filename="mask.jpg",
        mimetype="image/jpg",
    )


@webapp.route("/card_exists", methods=["POST"])
def card_exists():
    img = http.get_image_from_request(request)

    square_img = image.get_square_image(img)

    square_img_128 = square_img.resize((128, 128), Image.ANTIALIAS)

    is_card_exists = get_card_existence(square_img_128)

    return {"card_exists": is_card_exists}


@webapp.route("/get_card")
def get_card():
    return {"get_card": "ok"}


@webapp.route("/get_text")
def get_text():
    return {"get_text": "ok"}
