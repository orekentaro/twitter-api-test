from route.main_route import tweet_search
import tweepy
import key_dic
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
my_info = api.me()
Account = "@Eternal_door"  # 取得したいユーザーのユーザーIDを代入
tweets = api.user_timeline(Account, count=10, page=1)
num = 1  # ツイート数を計算するための変数
# for tweet in tweets:
#   print('アカウント名 : ', tweet.user.screen_name)  # ユーザー名
#   print('投稿日時 : ', tweet.created_at)      # 呟いた日時
#   print(tweet.text)                  # ツイート内容
#   print('いいね: ', tweet.favorite_count)  # ツイートのいいね数
#   print('RT : ', tweet.retweet_count)  # ツイートのリツイート数
#   print('ツイート数 : ', num)  # ツイート数
#   print('=' * 80)  # =を80個表示
#   num += 1  # ツイート数を計算ß
#   tweet_times = tweet.created_at + datetime.timedelta(hours=9)
#   days = datetime.datetime.now().date() - tweet_times.date()
#   print(type(days.days))

friends_ids = []

# ユーザーIDをリストに
for friend_id in tweepy.Cursor(api.friends_ids, user_id=my_info.id).items():
  friends_ids.append(friend_id)
count = 0
#IDからユーザーと最終更新時間を
for id in friends_ids:
  user = api.get_user(id)
  account = f'@{user.screen_name}'
  tweets = api.user_timeline(account, count=1)
  for tweet in tweets:
    days = datetime.datetime.now().date() - tweet.created_at.date()
    if days.days > 10:
      api.destroy_friendship(id)
      print(account, tweet.created_at)
      count += 1

print(f'{count}人消去')

