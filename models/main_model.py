from flask import render_template, request
from models.base_model import BaseModel
from common.library import tweet_gets, search_condition, save_user, save_tweet, save_hashtag
import datetime

class MainModel(BaseModel):
  def top_page(self):
    return render_template('main/top_page.html', home=True)

  def user_search(self):
    return render_template('main/user_search.html', user_search=True)

  def tweet_search(self):
    return render_template('main/tweet_search.html', tweet_search=True)

  def tweet_out(self):
    return render_template('main/tweet_out.html', tweet_out=True)

  def get_tweet(self):
    target = request.form['target']
    count = request.form['count']

    with self.start_transaction(False) as tx:
      """まず検索条件をインサート
      """
      #検索条件のシーケンス
      sql = "SELECT nextval('search_no_seq') as search_no_seq"
      search_no_seq = tx.find_one(sql)['search_no_seq']

      #検索条件保存
      search_condition(search_no_seq, target)

      """取得ツイートを変数に
      """
      tweets = tweet_gets(target, count)

      for tweet in tweets:
        '''for文でそれぞれのデータをインサート
        '''
        user = tweet.user  # ユーザー情報

        """ユーザー情報をテーブルに
        """
        #ユーザーシーケンス
        sql = "SELECT nextval('get_user_no_seq') as get_user_no_seq"
        get_user_no_seq = tx.find_one(sql)['get_user_no_seq']

        #ユーザー情報保存
        save_user(get_user_no_seq, user)


        """ツイート情報をテーブルに
        """
        #ツイート番号Seq
        sql = "SELECT nextval('tweet_id_seq') as tweet_id_seq"
        tweet_id_seq = tx.find_one(sql)['tweet_id_seq']

        #ツイート内容保存
        save_tweet(tweet_id_seq, search_no_seq, user, tweet)


        for hashtag in tweet.entities['hashtags']:
          if hashtag:
            '''投稿ツイートにハッシュタグがあれば
            '''
            # ハッシュタグ取り出す
            hashtag = hashtag['text']

            #ハッシュタグSeq
            sql = "SELECT nextval('tag_id_seq') as tag_id_seq"
            tag_id_seq = tx.find_one(sql)['tag_id_seq']

            #ハッシュタグ保存
            save_hashtag(tag_id_seq, hashtag, tweet_id_seq)
    return 'OK'