import io

from flask import send_file
from PIL import Image

from .. import settings
from ..exceptions import InvalidUsage


def get_file_from_request(request, rise_exc: bool = True):
    if "file" not in request.files:
        if rise_exc:
            raise InvalidUsage("You must send file")
        return None

    file = request.files["file"]
    if not file or file.filename == "":
        if rise_exc:
            raise InvalidUsage("You must send file")
        return None

    if not allowed_file(file.filename):
        if rise_exc:
            raise InvalidUsage("Only .jpg allowed")
        return None

    if file.mimetype not in settings.ALLOWED_MIMETYPES:
        if rise_exc:
            raise InvalidUsage("Only JPEG images allowed")
        return None

    # if file.content_length == 0:
    #     if rise_exc:
    #         raise InvalidUsage('Empty file')
    #     return None

    return file


def get_image_from_request(request, rise_exc: bool = True):
    file = get_file_from_request(request, rise_exc)
    img = Image.open(io.BytesIO(file.read()))
    print(f"filename: {file.filename}, mimetype: {file.mimetype}, size: {img.size}")
    return img


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in settings.ALLOWED_EXTENSIONS


def to_response(img: Image):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="jpeg")
    file_bytes = io.BytesIO(img_byte_arr.getvalue())
    return send_file(file_bytes, attachment_filename="output.jpg", mimetype="image/jpg")


# def save_file(file):
#     filename = secure_filename(file.filename)
#     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
