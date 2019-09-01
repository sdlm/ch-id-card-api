import io

from PIL import Image

from .. import settings
from ..exceptions import InvalidUsage


def get_file_from_request(request, rise_exc: bool = True):
    if "file" not in request.files:
        if rise_exc:
            raise InvalidUsage("You must send file")
        return None

    file = request.files["file"]
    print("- " * 10)
    print("file.filename: %s" % file.filename)
    print("file.content_length: %s" % file.content_length)
    print("file.mimetype: %s" % file.mimetype)
    print("file.mimetype_params: %s" % file.mimetype_params)
    print("- " * 10)
    if not file or file.filename == "":
        if rise_exc:
            raise InvalidUsage("You must send file")
        return None

    if not allowed_file(file.filename):
        if rise_exc:
            raise InvalidUsage("Only .jpg allowed")
        return None

    # if file.content_length == 0:
    #     if rise_exc:
    #         raise InvalidUsage('Empty file')
    #     return None

    return file


def get_image_from_request(request, rise_exc: bool = True):
    file = get_file_from_request(request, rise_exc)
    img = Image.open(io.BytesIO(file.read()))
    return img


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in settings.ALLOWED_EXTENSIONS
    )


def prepare_file_to_output(img: Image):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="jpeg")
    return io.BytesIO(img_byte_arr.getvalue())


# def save_file(file):
#     filename = secure_filename(file.filename)
#     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
