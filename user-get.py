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
tweets = api.user_timeline(Account, count=1, page=1)
# num = 1  # ツイート数を計算するための変数
# for tweet in tweets:
  # print('アカウント名 : ', tweet.user.screen_name)  # ユーザー名
  # print('投稿日時 : ', tweet.created_at)      # 呟いた日時
  # print(tweet.text)                  # ツイート内容
  # print('いいね: ', tweet.favorite_count)  # ツイートのいいね数
  # print('RT : ', tweet.retweet_count)  # ツイートのリツイート数
  # print('ツイート数 : ', num)  # ツイート数
  # print('=' * 80)  # =を80個表示
  # num += 1  # ツイート数を計算ß
# print(tweets[0].created_at + datetime.timedelta(hours=9))

friends_ids = []
# フォローした人のIDを全取得
# Cursor使うとすべて取ってきてくれるが，配列ではなくなるので配列に入れる
for friend_id in tweepy.Cursor(api.friends_ids, user_id=my_info.id).items():
  friends_ids.append(friend_id)
for i in range(1):
  user = api.get_user(friends_ids[i])
  account = f'@{user.screen_name}'
  tweets = api.user_timeline(account, count=1)
  for tweet in tweets:
    print(account, tweet.created_at)

  