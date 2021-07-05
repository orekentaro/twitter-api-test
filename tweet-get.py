import tweepy

""""
Twitterのキー
"""

# consumer_key = ""
# consumer_secret = ""
# access_token = ""
# access_token_secret = ""

consumer_key = "KaVvmuG05f4E3cuKcPlWtZCax"
consumer_secret = "1d6e3vSFv8gfb9Qf5vwQ02rAvEjO4iUZVcOiI5oZpIQFSW3AbO"
access_token = "1411142147328286720-4uu9o10X11v6UyaE8od2vuroj7FCBo"
access_token_secret = "aU7oB9o28797fLpWamoSb43Zrt3flwQWBFHTxKYFe63Fe"

"""
Twitterオブジェクトの生成
"""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


class Listener(tweepy.StreamListener):
  """ Handles tweets received from the stream. """

  def on_status(self, status):
    """ Prints tweet and hashtags """
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


listener = Listener()
stream = tweepy.Stream(auth, listener)
stream.filter(track=['#駆け出しエンジニアと繋がりたい'])
