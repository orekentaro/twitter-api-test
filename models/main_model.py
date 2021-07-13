from flask import render_template, request
from models.base_model import BaseModel
from common.library import tweet_gets
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
      sql = "SELECT nextval('search_no_seq') as search_no_seq"
      search_no_seq = tx.find_one(sql)['search_no_seq']
      sql = """
        INSERT INTO
          search_info(
            search_no,
            search_condition,
            get_at,
            status
          )
          VALUES(
            %s,%s,%s,%s
          )
        """
      insert_sarch_index = [
        search_no_seq,
        target,
        datetime.datetime.now(),
        '0'
      ]
      tx.save(sql, insert_sarch_index)

      #取得ツイートを変数に
      tweets = tweet_gets(target, count)

      n = 1
      for tweet in tweets:
        print(n)
        n+1
        '''for文でそれぞれのデータをインサート
        '''
        user = tweet.user  # ユーザー情報

        """ユーザー情報をテーブルに
        """
        sql = "SELECT nextval('get_user_no_seq') as get_user_no_seq"
        get_user_no_seq = tx.find_one(sql)['get_user_no_seq']
        sql = """
          INSERT INTO
            twitter_user(
              user_no,
              user_id,
              user_name,
              follow,
              follower,
              profile,
              tweet_count,
              status,
              created_id,
              created_at
            )
            VALUES(
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
          """
        insert_get_user_index = [
          get_user_no_seq,
          user.screen_name,
          user.name,
          user.friends_count,
          user.followers_count,
          user.description,
          user.statuses_count,
          0,
          'test_user',
          datetime.datetime.now()
        ]
        tx.save(sql, insert_get_user_index)


      # sql = "SELECT nextval('tweet_id_seq') as tweet_id_seq"
      # tweet_id_seq = tx.find_one(sql)['tweet_id_seq']
      # sql = """
      #     INSERT INTO
      #       tweet(
      #         tweet_id,
      #         search_no,
      #         user_id,
      #         post_content,
      #         favo_count,
      #         rt_count,
      #         reprly_count,
      #         post_time,
      #         status
      #       )
      #       VALUES(
      #         %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
      #       )
      #     """
      # insert_get_tweet_index = [
      #   tweet_id_seq,
      #   search_no_seq,
      #   user.screen_name,
      #   user.friends_count,
      #   tweet.text,
      #   tweet.favorite_count,
      #   tweet.retweet_count,
      #   0,  #リプライ数は要検討
      #   tweet.created_at.strftime("%Y/%m/%d %H:%M:%S"),
      #   0
      # ]
      # tx.save(sql, insert_get_tweet_index)

      # for hashtag in tweet.entities['hashtags']:
      #   '''ハッシュタグをインサート
      #   '''
      #   sql = """
      #     SELECT
      #       tag_id,
      #       detail,
      #       count
      #     FROM
      #       hashu_tag
      #     WHERE
      #       detail = %s
            
      #     """
      # hashtag_result = tx.find_one(sql, [hashtag])

      # if hashtag_result :
      #   '''すでに取得したハッシュタグがある場合はカウントを増やす
      #   '''
      #   tag_id = hashtag_result['tag_id']
      #   new_hashtag_count = hashtag_result['count'] = 1
      #   sql = """
      #       UPDATE
      #         hashu_tag
      #       SET
      #         count=%s
      #       WHERE
      #         info_id=%s
      #       """
      #   tx.save(sql, [new_hashtag_count, tag_id])

      # else:
      #   '''ハッシュタグがなければ追加
      #   '''
      #   sql = "SELECT nextval('tag_id_seq') as tag_id_seq"
      #   tag_id_seq = tx.find_one(sql)['tag_id_seq']

      #   sql = """
      #       INSERT INTO
      #         hash_tag(
      #           tag_id,
      #           detail,
      #           count
      #         )
      #       VALUES(
      #         %s,%s,%s
      #       )
      #       """
      #   tag_list = [tag_id_seq, tag_id_seq, 1]
      #   tx.save(sql, tag_list)

    return 'OK'