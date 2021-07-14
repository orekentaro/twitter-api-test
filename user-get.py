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

Account = "@Eternal_door"  # 取得したいユーザーのユーザーIDを代入
tweets = api.user_timeline(Account, count=1, page=1)
num = 1  # ツイート数を計算するための変数
for tweet in tweets:
  # print('アカウント名 : ', tweet.user.screen_name)  # ユーザー名
  # print('投稿日時 : ', tweet.created_at)      # 呟いた日時
  # print(tweet.text)                  # ツイート内容
  # print('いいね: ', tweet.favorite_count)  # ツイートのいいね数
  # print('RT : ', tweet.retweet_count)  # ツイートのリツイート数
  # print('ツイート数 : ', num)  # ツイート数
  # print('=' * 80)  # =を80個表示
  # num += 1  # ツイート数を計算
  print(tweet.created_at)

