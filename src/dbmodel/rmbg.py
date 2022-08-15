"""Database Schema Defination module."""

import os
from datetime import datetime

from flask import url_for

from ..extension import database
from ..config import config_object as config
from ..utility import build_input_img_name, build_output_img_name


class RemoveBG(database.Model):
    """RMBGMaster Schema defination."""

    __tablename__ = "rmbg"
    task_id = database.Column(database.Integer, primary_key=True)

    upload_type = database.Column(database.String(6), nullable=True)

    upload_date = database.Column(
        database.Date, nullable=False, default=datetime.utcnow()
    )
    input_file = database.Column(database.String(20), nullable=False, unique=True)

    mask_file = database.Column(database.String(20), nullable=False, unique=True)

    output_file = database.Column(database.String(20), nullable=True, unique=True)

    # final_result = database.relationship("AddBG", backref="rmbg", lazy="joined")

    def __init__(self, filename, uploadtype):
        """Pass Filename as argument.

        Args:
            filename (String): File name
            upload_date ([type], optional): [description]. Defaults to datetime.now().
        """
        self.upload_type = uploadtype
        self.upload_date = datetime.utcnow()
        self.input_file = build_input_img_name(filename, self.upload_date)

        self.mask_file = build_output_img_name(filename, self.upload_date, "mask")

        self.output_file = build_output_img_name(filename, self.upload_date, "bgcr")

    def serialize(self):
        """Returns Image as object.

        Returns:
            [object]: Image Object
        """
        return {
            "task_id": self.task_id,
            "upload_type": self.upload_type,
            "upload_date": self.upload_date,
            "input_file": self.input_file,
            "input_url": self.input_image_url,
            "mask_file": self.mask_file,
            "mask_url": self.mask_image_url,
            "output_file": self.output_file,
            "output_url": self.output_image_url,
        }

    def __repr__(self):
        """Repr method for Image .

        Returns:
            [String]: image id : Image name
        """
        return f"{self.task_id}, {self.input_file} {self.mask_file} {self.output_file}"

    @property
    def input_image_path(self):
        return os.path.join(config.UPLOAD_FOLDER, self.input_file)

    @property
    def input_image_url(self):
        return url_for("download_file", name=self.input_file)

    @property
    def mask_image_path(self):
        return os.path.join(config.UPLOAD_FOLDER, self.mask_file)

    @property
    def mask_image_url(self):
        return url_for("download_file", name=self.mask_file)

    @property
    def output_image_path(self):
        return os.path.join(config.UPLOAD_FOLDER, self.output_file)

    @property
    def output_image_url(self):
        return url_for("download_file", name=self.output_file)
