from typing import Tuple

import numpy as np
from PIL import Image


def get_mean_color(arr: np.array) -> Tuple[int, int, int]:
    assert len(arr.shape) == 3, "Only for RGB image mode"
    assert arr.shape[2] == 3, "Three dimensions expected"
    mean_color = np.mean(
        np.mean(arr, axis=0, keepdims=True), axis=1, keepdims=True
    ).squeeze()
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
