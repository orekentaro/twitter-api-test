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

# ツイートの投稿
api.update_status("test")
