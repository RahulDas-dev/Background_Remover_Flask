import os


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = os.environ.get("SECRET_KEY")
    FLASK_APP = os.environ.get("FLASK_APP")
    FLASK_DEBUG = True if os.environ.get("FLASK_DEBUG") == "1" else False

    # Production and Development Specific Environment
    TESTING = False
    DEBUG = True if FLASK_DEBUG else False

    # Database
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):  # noqa N802
        if self.FLASK_DEBUG:  # for Development
            return f"sqlite:///{os.path.join(self.BASE_DIR,'database','sqlite.dev.db')}"
        else:  # for production
            # return os.environ.get("PROD_DATABASE_URI")
            return (
                f"sqlite:///{os.path.join(self.BASE_DIR,'database','sqlite.prod.db')}"
            )

    # Upload directory
    ALLOWED_EXTENSIONS = {"jpg", "png", "jpeg", "PNG"}

    @property
    def UPLOAD_FOLDER(self):  # noqa N802
        return os.path.join(self.BASE_DIR, "image_store")

    # Model_path
    MODEL_FILE_NAME = os.environ.get("MODEL_NAME", "u2net.onnx")

    @property
    def MODEL_PATH(self):  # noqa N802
        return os.path.join(self.BASE_DIR, "trained_model", self.MODEL_FILE_NAME)


config_object = Config()
