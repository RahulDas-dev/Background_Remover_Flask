from datetime import datetime
from typing import Literal

from werkzeug.utils import secure_filename

from .config import config_object as config


def build_input_img_name(filename_: str, created_at_: datetime) -> str:
    """Returns modified image name.

    Returns:
        [string]: Returns modified image name
    """
    filename = secure_filename(filename_)
    name_arry = filename.split(".")
    name = f'{".".join(name_arry[:-1])}_{created_at_.strftime("%Y-%m-%d_%H-%M-%S")}'
    extn = name_arry[-1]
    return f"{name}.{extn}"


def build_output_img_name(
    filename_: str,
    created_at_: datetime,
    type_: Literal["mask", "bgcr", "bgad"] = "mask",
    extn_: Literal["png", "jpeg"] = "png",
) -> str:
    """Returns modified image name.

    Returns:
        [string]: Returns modified image name
    """
    name_arry = filename_.split(".")
    name = f'{type_}_{".".join(name_arry[:-1])}_{created_at_.strftime("%Y-%m-%d_%H-%M-%S")}'
    return f"{name}.{extn_}"


def allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS
    )
