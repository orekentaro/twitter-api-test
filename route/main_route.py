from flask import Blueprint
from models.main_model import MainModel

main_route = Blueprint('main_route', __name__, url_prefix='/offgrid_twitter_api/')
MainModel = MainModel()


@main_route.route('/login')
def login():
  """ログイン画面"""
  return MainModel.login()


@main_route.route('/login', methods=['POST'])
def login_check():
  """ログイン処理"""
  return MainModel.login_check()


@main_route.route('/log_out')
def log_out():
  """ログアウト処理"""
  return MainModel.log_out()


@main_route.route('/create_account')
def create_account():
  """アカウント作成画面"""
  return MainModel.create_account()


@main_route.route('/create_account_confirm', methods=['POST'])
def create_account_confirm():
  """アカウント作成確認画面"""
  return MainModel.create_account_confirm()


@main_route.route('/created_account', methods=['POST'])
def created_account():
  """アカウント作成確認画面"""
  return MainModel.created_account()


@main_route.route('/dashboard')
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


@main_route.route('/get_tweet_details/<id>')
def get_tweet_details(id):
  """取得ツイート詳細画面を表示するルート"""
  return MainModel.get_tweet_details(id)


@main_route.route('/get_user', methods=['POST'])
def get_user():
  """ツイート出力画面を表示するルート"""
  return MainModel.get_user()


@main_route.route('/search_word', methods=['POST'])
def search_word():
  """文字検索出力画面を表示するルート"""
  return MainModel.search_word()


@main_route.route('/search_tag', methods=['POST'])
def search_tag():
  """文字検索出力画面を表示するルート"""
  return MainModel.search_tag()


@main_route.route('/user_list')
def user_list():
  """ユーザー一覧を表示するルート"""
  return MainModel.user_list()


@main_route.route('/get_new_record')
def get_new_record():
  """ユーザー一覧を表示するルート"""
  return MainModel.get_new_record()
