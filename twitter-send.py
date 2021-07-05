import tweepy

""""
Twitterのキー
"""
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

"""
Twitterオブジェクトの生成
"""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# ツイートの投稿
api.update_status("test")
