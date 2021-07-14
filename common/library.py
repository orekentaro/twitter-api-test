import tweepy
import key_dic
from models.main_model import BaseModel
import datetime
""""
Twitterのキー
"""
consumer_key = key_dic.api_key_dic["consumer_key"]
consumer_secret = key_dic.api_key_dic["consumer_secret"]
access_token = key_dic.api_key_dic["access_token"]
access_token_secret = key_dic.api_key_dic["access_token_secret"]

"""
Twitterオブジェクトの生成
"""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

api = tweepy.API(auth)

#DB用のインスタンス生成
BaseModel = BaseModel()


def set_gmt_jp(time):
  """ツイート時間を日本時刻に戻す
    Args:
      time : twitterのtweet.created_at
    Returns:
      True:
        日本時間になって返ってくる
  """
  return time + datetime.timedelta(hours=9)

def tweet_gets(target , count):
  """ツイート文字検索
    Args:
      target(string):検索したい文字列
      count(int):検索したい数
    Returns:
      True:
        取得したツイートの情報がjsonで返ってくる
      False:
    Examples:
      フリーワード、ハッシュダグでツイートを検索する関数
  """
  tweets = api.search(q=[target], count=count)
  return tweets


def search_condition(search_no_seq, target, status):
  """検索条件保存
    Args:
      search_no_seq(int): 検索条件のシーケンス
      target(string):フォームから取得した検索条件
      status(string): 
        0: 文字列検索
        1: ユーザー検索
    Returns:
      なし
    Examples:
      フリーワード、ハッシュダグ、ユーザー検索で使用する
  """
  with BaseModel.start_transaction(False) as tx:
    sql = """
      INSERT INTO
        search_info(
          search_no,
          search_condition,
          get_id,
          get_at,
          status
        )
        VALUES(
          %s,%s,%s,%s,%s
        )
      """
    insert_sarch_index = [
      search_no_seq,
      target,
      'ながと',
      datetime.datetime.now(),
      status
    ]
    tx.save(sql, insert_sarch_index)

def save_user(get_user_no_seq, user):
  """ユーザー保存
    Args:
      get_user_no_seq(int): ユーザーのシーケンス
      user(json):ツイート情報からユーザーの情報だけを取得したjson
    Returns:
      なし
    Examples:
      フリーワード、ハッシュダグ、ユーザー検索で使用する
  """
  with BaseModel.start_transaction(False) as tx:
    sql = """
      INSERT INTO
        twitter_user(
          user_no,
          user_id,
          user_name,
          follow,
          follower,
          profile,
          tweet_count,
          status
        )
        VALUES(
          %s,%s,%s,%s,%s,%s,%s,%s
        )
      """
    insert_get_user_index = [
      get_user_no_seq,
      user.screen_name,
      user.name,
      user.friends_count,
      user.followers_count,
      user.description,
      user.statuses_count,
      "0",
    ]
    tx.save(sql, insert_get_user_index)

def save_tweet(tweet_id_seq, search_no_seq, user, tweet):
  """ツイート保存
    Args:
      tweet_id_seq(int): ツイートのシーケンス
      search_no_seq(int): 検索条件のシーケンス
      user(json):ツイート情報からユーザーの情報だけを取得したjson
      tweet(json):ツイート情報のjson
    Returns:
      なし
    Examples:
      フリーワード、ハッシュダグ、ユーザー検索で使用する
  """
  tweet.created_at = set_gmt_jp(tweet.created_at)
  with BaseModel.start_transaction(False) as tx:
    sql = """
      INSERT INTO
        tweet(
          tweet_id,
          search_no,
          user_id,
          post_content,
          favo_count,
          rt_count,
          reprly_count,
          post_time,
          status
        )
        VALUES(
          %s,%s,%s,%s,%s,%s,%s,%s,%s
        )
      """
    insert_get_tweet_index = [
      tweet_id_seq,
      search_no_seq,
      user.screen_name,
      tweet.text,
      tweet.favorite_count,
      tweet.retweet_count,
      0,
      tweet.created_at.strftime("%Y/%m/%d %H:%M:%S"),
      "0"
    ]
    tx.save(sql, insert_get_tweet_index)

def save_hashtag(tag_id_seq, hashtag, tweet_id_seq):
  """ハッシュタグ保存
    Args:
      tag_id_seq(int): ハッシュタグのシーケンス
      tweet_id_seq(int): ツイート番号のシーケンス
      hashtag(string):ツイート情報かハッシュタグを取得した文字列
    Returns:
      なし
    Examples:
      フリーワード、ハッシュダグ、ユーザー検索で使用する
  """
  with BaseModel.start_transaction(False) as tx:
    sql = """
      INSERT INTO
        hash_tag(
          tag_id,
          detail,
          tweet_id
        )
      VALUES(
        %s,%s,%s
      )
      """
    tag_list = [tag_id_seq, hashtag, tweet_id_seq]
    tx.save(sql, tag_list)

def date_format(hiduke):
  """日付のフォーマット（%Y/%m/%d %H:%M or %Y/%m/%d）
    Args:
      hiduke(datetime.date か datetime.datetime型):主にnow()やtoday()で持ってきた時間か、ＤＢ内の時間に使用
    Returns:
      True:
        datetime.date(2021, 3, 10) => 例 2021/03/10
        datetime.datetime(2021, 3, 10, 20, 17, 46, 726575) => 例 2021/03/10 20:17
      False:
        型が上記の2つ以外のものだったらexceptでエラーを出す。
    Examples:
      引数にdatetime.date か datetime.datetime型を入れるだけでフォーマット完了
  """
  try:
    if type(hiduke) is datetime.datetime:
      return hiduke.strftime("%Y/%m/%d %H:%M")
    elif type(hiduke) is datetime.date:
      return hiduke.strftime("%Y/%m/%d")
    elif hiduke is None:
      return None
  except Exception:
    raise Exception("日付の形式が正しくありません")

def get_user(target, count):
  """ユーザー別ツイート検索
    Args:
      target(string):検索したい文字列
      count(int):検索したい数
    Returns:
      True:
        取得したツイートの情報がjsonで返ってくる
      False:
    Examples:
      @user_idでツイートを検索する関数
  """
  tweets = api.user_timeline(target, count=count)
  return tweets

def search_infos(status):
  """ユーザー別ツイート検索
    Args:
      status(string):
        :"si.status = '1'" :ユーザー検索
        :"si.status = '0'" :ツイート検索
    Returns:
      True:
        取得したツイートの情報がjsonで返ってくる
      False:
    Examples:
      @user_idでツイートを検索する関数
  """
  with BaseModel.start_transaction() as tx:
    sql = f"""
      SELECT
        si.search_no as sn,
        search_condition,
        get_id,
        get_at,
        tw.tw_count,
        si.status
      FROM
        search_info si
      LEFT JOIN
        (SELECT COUNT(*) as tw_count , search_no FROM tweet GROUP BY search_no ) tw
      ON 
        si.search_no = tw.search_no
      WHERE
        {status}
      ORDER BY
        get_at DESC
      """
    search_infos = tx.find_all(sql)

    for info in search_infos:
      info['get_at'] = date_format(info['get_at'])
    
  return search_infos
