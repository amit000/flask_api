import traceback

from flask import request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask_uploads import UploadNotAllowed

from libs import image_helper
from libs.strings import gettext
from schemas.images import ImageSchema

image_schema = ImageSchema()


class ImageUpload(Resource):
    @jwt_required
    def post(self):
        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"

        try:
            basename = image_helper.save_image(data["image"], folder=folder)
            return {"message": gettext("image_IMAGE_SAVED").format(basename)}

        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return (
                {"message": gettext("image_ILLEGAL_EXTENSION").format(extension)},
                400,
            )


class Image(Resource):
    @jwt_required
    def get(self, filename: str):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"

        if not image_helper.is_filename_safe(filename):
            return {"message": gettext("image_FILENAME_NOT_SAFE").format(filename)}, 400

        try:
            return send_file(image_helper.get_path(filename, folder=folder))
        except FileNotFoundError:
            return {"message": gettext("image_FILE_NOT_FOUND")}, 404

    @jwt_required
    def delete(self, filename: str):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"

        if not image_helper.is_filename_safe(filename):
            return {"message": gettext("image_FILENAME_NOT_SAFE").format(filename)}, 400

        try:
            image_helper.remove(filename, folder=folder)
            return {
                "message": gettext("image_FILE_SUCCESSFULLY_DELETED").format(filename)
            }
        except FileNotFoundError:
            return {"message": gettext("image_FILE_NOT_FOUND")}, 404
        except:
            traceback.print_exc()
            return {"message": gettext("image_DELETE_FAILED")}, 500
