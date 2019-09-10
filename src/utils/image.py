import math
from typing import Tuple

import numpy as np
from PIL import Image


def get_mean_color(arr: np.array) -> Tuple[int, int, int]:
    assert len(arr.shape) == 3, "Only for RGB image mode"
    assert arr.shape[2] == 3, "Three dimensions expected"
    mean_color = np.mean(np.mean(arr, axis=0, keepdims=True), axis=1, keepdims=True).squeeze()
    return tuple(mean_color.astype(int).tolist())  # type: ignore


def get_square_size(arr: np.array) -> Tuple[int, int]:
    new_dim = max(arr.shape[0], arr.shape[1])
    return new_dim, new_dim


def get_offset(background: Image, img: Image) -> Tuple[int, int]:
    img_w, img_h = img.size
    bg_w, bg_h = background.size
    return (bg_w - img_w) // 2, (bg_h - img_h) // 2


def get_square_image(img: Image) -> Image:
    arr = np.array(img, dtype=np.uint8)
    square_img = Image.new("RGB", get_square_size(arr), get_mean_color(arr))
    square_img.paste(img, get_offset(square_img, img))
    return square_img


def get_card(img: Image, coords: np.array) -> Image:
    img_arr = np.array(img)

    # shift
    center = coords.sum(axis=0) / 4
    shift_x = img_arr.shape[0] / 2 - center[0]
    shift_y = img_arr.shape[1] / 2 - center[1]
    img_arr = shift_image(img_arr, shift_x, shift_y)
    coords = shift_coords(coords, shift_x, shift_y)

    # rotate
    p1 = coords[0]
    p2 = coords[1]
    delta_x = p2[0] - p1[0]
    delta_y = p2[1] - p1[1]
    theta_radians = math.atan2(-delta_y, delta_x)
    angle = -theta_radians / math.pi * 180
    img_arr = rotate_image(img_arr, angle)
    coords = rotate_coords(coords, theta_radians, img_arr.shape, radians=True)

    # crop
    a = coords.min(axis=0).astype(int)
    b = coords.max(axis=0).astype(int)
    box = (a.item(0), a.item(1), b.item(0), b.item(1))
    return Image.fromarray(img_arr).crop(box)


def shift_coords(coords, shift_x, shift_y):
    new_coords = np.copy(coords)
    new_coords[:, 0] = new_coords[:, 0] + shift_x
    new_coords[:, 1] = new_coords[:, 1] + shift_y
    return new_coords


def shift_image(img_arr: np.array, shift_x, shift_y) -> np.array:
    layers_map = {1: "L", 3: "RGB", 4: "RGBA"}
    layer_count = img_arr.shape[2] if len(img_arr.shape) == 3 else 1
    image = Image.fromarray(img_arr.astype("uint8"), layers_map[layer_count])
    image = image.transform(image.size, Image.AFFINE, (1, 0, -shift_x, 0, 1, -shift_y))
    return np.array(image)


def rotate_coords(coords, angle, img_shape, radians: bool = False):
    a = angle
    if not radians:
        a = angle / 180.0 * np.pi
    rotation_matrix = np.matrix(((np.cos(a), -np.sin(a)), (np.sin(a), np.cos(a))))
    x_center = img_shape[0] / 2
    y_center = img_shape[1] / 2
    coords_ = np.copy(coords)
    coords_[:, 0] = coords_[:, 0] - x_center
    coords_[:, 1] = coords_[:, 1] - y_center
    new_coords = coords_ @ rotation_matrix
    new_coords[:, 0] = new_coords[:, 0] + x_center
    new_coords[:, 1] = new_coords[:, 1] + y_center
    return new_coords


def rotate_image(img_arr: np.array, angle) -> np.array:
    layers_map = {1: "L", 3: "RGB", 4: "RGBA"}
    layer_count = img_arr.shape[2] if len(img_arr.shape) == 3 else 1
    image = Image.fromarray(img_arr.astype("uint8"), layers_map[layer_count])
    image = image.rotate(angle, resample=Image.BILINEAR, expand=False)
    return np.array(image)
