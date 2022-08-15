"""Database Schema Defination module."""

import os
from datetime import datetime

from flask import url_for

from ..config import config_object as config
from ..extension import database
from ..utility import build_input_img_name, build_output_img_name


class AddBG(database.Model):
    """Image Schema defination."""

    __tablename__ = "adbg"
    cascade_id = database.Column(database.Integer, primary_key=True)

    task_id = database.Column(database.Integer, database.ForeignKey("rmbg.task_id"))

    upload_date = database.Column(
        database.Date, nullable=False, default=datetime.utcnow()
    )
    input_file = database.Column(database.String(20), nullable=False)
    output_file = database.Column(database.String(20), nullable=True)

    def __init__(self, taskid, filename):
        """Pass Filename as argument.

        Args:
            filename (String): File name
            upload_date ([type], optional): [description]. Defaults to datetime.now().
        """
        self.task_id = taskid
        self.upload_date = datetime.now()

        self.input_file = build_input_img_name(filename, self.upload_date)

        self.output_file = build_output_img_name(filename, self.upload_date, "bgad")

    def serialize(self):
        """Returns Image as object.

        Returns:
            [object]: Image Object
        """
        return {
            "task_id": self.task_id,
            "upload_date": self.upload_date,
            "input_file": self.input_file,
            "input_url": self.input_image_url,
            "output_file": self.output_file,
            "output_url": self.output_image_url,
        }

    def __repr__(self):
        """Repr method for Image .

        Returns:
            [String]: image id : Image name
        """
        return f"{self.task_id} : {self.input_file} {self.output_file}"

    @property
    def input_image_url(self):
        return url_for("download_file", name=self.input_file)

    @property
    def input_image_path(self):
        return os.path.join(config.UPLOAD_FOLDER, self.input_file)

    @property
    def output_image_url(self):
        return url_for("download_file", name=self.output_file)

    @property
    def output_image_path(self):
        return os.path.join(config.UPLOAD_FOLDER, self.output_file)
