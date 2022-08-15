from flask_sqlalchemy import SQLAlchemy

from .mlmodel.model import ModelExtension as Model

ml_model = Model()
database = SQLAlchemy()
