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


class Listener(tweepy.StreamListener):
  """ 指定のハッシュタグの最新のツイートを随時取得していく """

  def on_status(self, status):
    """ 情報を出力 """
    print('------------------------------')
    print(f"ユーザーID：{status.user.screen_name}")
    print(f"プロフィール：{status.user.description}")
    print(f"ツイート内容：{status.text}")
    print(f"投稿日時：{status.created_at}")
    for hashtag in status.entities['hashtags']:
      print(f"使用していたハッシュタグ：{hashtag['text']}"),
    print("")
    return True

  def on_error(self, status_code):
    print('Got an error with status code: ' + str(status_code))
    return True

  def on_timeout(self):
    print('Timeout...')
    return True


# 取得したいハッシュタグをこの変数に入れる。
sarch_hashtag = '#駆け出しエンジニアと繋がりたい'
listener = Listener()
stream = tweepy.Stream(auth, listener)
stream.filter(track=[sarch_hashtag])
