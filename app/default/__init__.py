from flask import Blueprint
from config import Config

default = Blueprint('cast', __name__, static_folder=Config.STATIC_FOLDER, static_url_path='')
registro = Blueprint('registro', __name__, static_folder=Config.STATIC_FOLDER, static_url_path='')
quote = Blueprint('quote', __name__, static_folder=Config.QUOTE_FOLDER, static_url_path='')
weight = Blueprint('weight', __name__, static_folder=Config.WEIGHT_FOLDER, static_url_path='')
from . import routes
