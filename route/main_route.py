from flask import Blueprint
from models.main_model import MainModel

main_route = Blueprint('main_route', __name__, url_prefix='/offgrid_twitter_api/')
MainModel = MainModel()


@main_route.route('/')
def top_page():
  """ログイン画面を表示するルート"""
  return MainModel.top_page()