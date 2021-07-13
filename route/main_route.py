from flask import Blueprint
from models.main_model import MainModel

main_route = Blueprint('main_route', __name__, url_prefix='/offgrid_twitter_api/')
MainModel = MainModel()


@main_route.route('/')
def top_page():
  """トップページを表示するルート"""
  return MainModel.top_page()

@main_route.route('/user_search')
def user_search():
  """ユーザー検索画面を表示するルート"""
  return MainModel.user_search()

@main_route.route('/tweet_search')
def tweet_search():
  """ツイート検索画面を表示するルート"""
  return MainModel.tweet_search()

@main_route.route('/tweet_out')
def tweet_out():
  """ツイート出力画面を表示するルート"""
  return MainModel.tweet_out()

@main_route.route('/get_tweet', methods=['POST'])
def get_tweet():
  """ツイート出力画面を表示するルート"""
  return MainModel.get_tweet()