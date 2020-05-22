import os
import re
from typing import Union

from flask_uploads import UploadSet, IMAGES
from werkzeug.datastructures import FileStorage

IMAGE_SET = UploadSet("images", IMAGES)


def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    path = IMAGE_SET.save(image, folder, name)
    return os.path.split(path)[1]


def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    if isinstance(file, FileStorage):
        return file.filename
    return file


def get_extension(image: Union[str, FileStorage]) -> str:
    filename = _retrieve_filename(image)
    return os.path.splitext(filename)[1]


def is_filename_safe(file: Union[str, FileStorage]) -> bool:
    filename = _retrieve_filename(file)
    allowed_format = "|".join(IMAGES)
    # format IMAGES into regex, eg: ('jpeg','png') --> 'jpeg|png'
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None


def get_path(filename: str = None, folder: str = None) -> str:
    return IMAGE_SET.path(filename, folder)


def remove(filename, folder) -> None:
    os.remove(get_path(filename, folder=folder))
