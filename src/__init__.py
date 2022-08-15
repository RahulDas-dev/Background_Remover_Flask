"""Application Init Module ."""

from dotenv import load_dotenv
from flask import Flask

from .config import config_object as config
from .extension import database, ml_model
from .mlmodel.model import ModelExtension as Model

load_dotenv()

app = Flask(__name__, static_folder="../static")

app.config.from_object(config)

ml_model.init_app(app)
database.init_app(app)

from .dbmodel import *  # noqa: E402

with app.app_context():
    database.create_all()

from . import routes  # noqa: E402
