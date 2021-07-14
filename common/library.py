import tweepy
import key_dic

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

