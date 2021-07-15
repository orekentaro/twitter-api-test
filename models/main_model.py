from flask import render_template, request, redirect, url_for, flash
from models.base_model import BaseModel
from common.library import tweet_gets, search_condition, save_user, save_tweet, save_hashtag, get_user, search_infos, check_form, tweet_list
import datetime

class MainModel(BaseModel):
  def login(self):
    return render_template('main/login.html')



  def top_page(self):
    with self.start_transaction() as tx:
      sql = f"""
        SELECT
        DISTINCT
          user_id,
          user_name,
          follow,
          follower,
          profile,
          tweet_count,
          get_time
        FROM
          twitter_user t1
        WHERE get_time = (
          SELECT MAX(get_time)
          FROM twitter_user t2
          WHERE t1.user_id = t2.user_id
          )
        """
      users = tx.find_all(sql)

    return render_template('main/top_page.html', home=True, users=users)

  def user_search(self):
    """ユーザー検索画面アンド一覧
    """
    return render_template('main/user_search.html', user_search=True, search_infos=search_infos("WHERE si.status = '1'"))

  def tweet_search(self):
    """ツイート検索画面アンド一覧
    """
    return render_template('main/tweet_search.html', tweet_search=True, search_infos=search_infos("WHERE si.status = '0'"))

  def tweet_out(self):
    return render_template('main/tweet_out.html', tweet_out=True)

  def get_tweet(self):
    """ツイート取得処理
    """
    target = request.form['target']
    count = request.form['count']

    validation_flag = check_form(target, count, '0')
    if validation_flag:
      flash(validation_flag['message'], "alert-danger")
      return redirect(url_for('main_route.tweet_search'))
    
    try:
      with self.start_transaction(False) as tx:
        """まず検索条件をインサート
        """
        #検索条件のシーケンス
        sql = "SELECT nextval('search_no_seq') as search_no_seq"
        search_no_seq = tx.find_one(sql)['search_no_seq']

        #検索条件保存
        search_condition(search_no_seq, target, '0')

        """取得ツイートを変数に
        """
        tweets = tweet_gets(target, int(count))

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
      flash(f"ツイートを取得しました!　（{target}:{count}件）", "alert-primary")
      return redirect(url_for('main_route.tweet_search'))
    except:
      flash(f"ツイートを取得できませんでした。", "alert-danger")
      return redirect(url_for('main_route.tweet_search'))

  def get_tweet_details(self, id):
    """ツイート検索画面アンド一覧
    """
    return render_template('main/get_tweet_details.html',get_tweets=tweet_list(f'WHERE search_no={id}'), tweet_search=True)

  def get_user(self):
    target = request.form['target']
    count = request.form['count']

    validation_flag = check_form(target, count, '1')
    if validation_flag:
      flash(validation_flag['message'], "alert-danger")
      return redirect(url_for('main_route.user_search'))

    try:
      with self.start_transaction(False) as tx:
        """まず検索条件をインサート
        """
        #検索条件のシーケンス
        sql = "SELECT nextval('search_no_seq') as search_no_seq"
        search_no_seq = tx.find_one(sql)['search_no_seq']

        #検索条件保存
        search_condition(search_no_seq, target, '1')

        """取得ツイートを変数に
        """
        tweets = get_user(target, int(count))

        #ユーザー情報を変数に
        user = tweets[0].user

        #ユーザーシーケンス
        sql = "SELECT nextval('get_user_no_seq') as get_user_no_seq"
        get_user_no_seq = tx.find_one(sql)['get_user_no_seq']

        #ユーザー情報保存
        save_user(get_user_no_seq, user)

        for tweet in tweets:
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

      flash(f"ツイートを取得しました!　（{target}:{count}件）", "alert-primary")
      return redirect(url_for('main_route.user_search'))

    except:
      flash(f"ツイートを取得できませんでした。", "alert-danger")
      return redirect(url_for('main_route.user_search'))