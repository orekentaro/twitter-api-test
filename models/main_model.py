from os import name
import re
from flask import render_template, request, redirect, url_for, flash, session
from models.base_model import BaseModel
from common.library import date_format, tweet_gets, search_condition, save_user, save_tweet, save_hashtag, get_user, search_infos, check_form, tweet_list
import datetime
from werkzeug.security import check_password_hash, generate_password_hash

class MainModel(BaseModel):
  def login(self):
    return render_template('main/login.html')
  
  def log_out(self):
    session.clear()
    flash("ログアウト成功！", "alert-primary")
    return redirect(url_for('main_route.login'))

  def login_check(self):
    admin_id = request.form['user_id']
    password = request.form['password']
    with self.start_transaction() as tx:
      sql = """
          SELECT
            admin_id,
            name,
            email,
            password,
            init_flag,
            lock_flag,
            dummy_password,
            status
          FROM
            admin_user
          WHERE
            admin_id = %s
          """
      user = tx.find_one(sql, [admin_id])

    if not user:
      """IDが未登録の場合"""
      flash("アカウントが登録されていません", "alert-danger")
      return redirect('main_route.login')

    if user['lock_flag'] == "1":
      """アカウントにロックフラグが立っている場合"""
      flash("アカウントがロックされています", "alert-danger")
      return redirect(url_for('main_route.login'))

    if user['status'] == "9":
      """アカウントが削除済の場合"""
      flash("アカウントが削除されています。管理者に連絡してください。", "alert-danger")
      return redirect(url_for('main_route.login'))

    if user['init_flag'] == '1':
      '''初期化フラグが立っている場合'''
      if password == user['dummy_password']:
        '''仮パスワードパスワードが一致した場合'''
        return render_template('system/user_edit.html', new_add=True, user=user)
      else:
        flash("仮パスワードが間違ってます。", "alert-danger")
        return redirect(url_for('main_route.login'))

    if not check_password_hash(user["password"], password):
      flash("パスワードが間違ってます。", "alert-danger")
      return redirect(url_for('main_route.login'))

    session['login_user'] = admin_id
    flash("ログイン成功！", "alert-primary")
    return redirect(url_for('main_route.top_page'))
  
  def create_account(self):
    return render_template('main/create_account.html', create=True)
  
  def create_account_confirm(self):
    password_length = len(request.form['password'])
    with self.start_transaction() as tx:
      sql = """
            SELECT
              admin_id,
              name,
              email,
              password,
              init_flag,
              lock_flag,
              dummy_password,
              status
            FROM
              admin_user
            WHERE
              admin_id = %s
            """
      user = tx.find_one(sql, [request.form['user_id']])

      if user:
        flash("すでにアカウントが登録されています", "alert-danger")
        return redirect(url_for('main_route.create_account'))
      
      if request.form['password'] != request.form['confirm_pass']:
        flash("パスワードが一致しません", "alert-danger")
        return render_template('main/create_account.html', user_id=request.form['user_id'], name=request.form['name'], email=request.form['email'])



    return render_template('main/create_account.html', confirm=True, user_id=request.form['user_id'], name=request.form['name'], email=request.form['email'], password=request.form['password'], confirm_pass=request.form['confirm_pass'], len = password_length)
  
  def created_account(self):
    user_id = request.form['user_id']
    name = request.form['name']
    email = request.form['email']
    password = generate_password_hash(request.form['password'])
    with self.start_transaction(False) as tx:
      sql = """
            INSERT INTO
              admin_user(
                admin_id,
                name,
                email,
                password,
                status,
                created_id,
                updated_id,
                created_at,
                updated_at
              )
              VALUES(
                %s,%s,%s,%s,%s,%s,%s,%s,%s
              )
            """
      insert_admin_list = [
        user_id, name, email, password, '0', 'create', 'create', datetime.datetime.now(), datetime.datetime.now()
        ]

      session['login_user'] = user_id
      flash("アカウントを作成しました！", "alert-primary")
      tx.save(sql, insert_admin_list)

    return redirect(url_for('main_route.top_page'))

  def top_page(self):
    with self.start_transaction() as tx:
      sql = f"""
        SELECT
          tu.user_id,
          tu.user_name,
          follow,
          follower,
          profile,
          tweet_count,
          get_time
        FROM
          twitter_user tu
        JOIN (SELECT MAX(user_no) as user_no, user_id FROM twitter_user GROUP BY user_id) max
          ON
            tu.user_no = max.user_no
        """
      users = tx.find_all(sql)

      for user in users:
        user['get_time'] = date_format(user['get_time'])

      sql = f"""
        SELECT
          tu.user_id,
          tu.user_name,
          follow,
          follower,
          profile,
          tweet_count,
          get_time
        FROM
          twitter_user tu
        JOIN admin_user au
          ON
            tu.user_id = au.admin_id
        JOIN (SELECT MAX(user_no) as user_no, user_id FROM twitter_user GROUP BY user_id) max
          ON
            tu.user_no = max.user_no
        """
      admin_users = tx.find_all(sql)

      for admin_user in admin_users:
        admin_user['get_time'] = date_format(admin_user['get_time'])


    return render_template('main/top_page.html', home=True, users=users, admin_users=admin_users)

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
    """取得ツイート詳細画面
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