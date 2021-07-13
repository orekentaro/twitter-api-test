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
tweets = api.search(q=['#Python'], count=10)

for tweet in tweets:
  print('------------------------------')
  print(f"ユーザーID：{tweet.user.screen_name}")
  print(f"プロフィール：{tweet.user.description}")
  print(f"ツイート内容：{tweet.text}")
  print(f"投稿日時：{tweet.created_at}")
  for hashtag in tweet.entities['hashtags']:
    print(f"使用していたハッシュタグ：{hashtag['text']}")
  print("")