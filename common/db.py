import psycopg2
from psycopg2.extras import DictCursor


class DbConnecter():
  def __init__(self, dbname, host, user, password):
    self.__setting(dbname, host, user, password)

  def __setting(self, dbname, host, user, password):
    self.__dbname = dbname
    self.__host = host
    self.__user = user
    self.__password = password

  def get_connect(self):
    return psycopg2.connect(f"dbname={self.__dbname} host={self.__host} user={self.__user} password={self.__password}")


class Transaction():
  """ トランザクションを処理を実行するためのクラス
      connector: DBConnecterクラスを使用したDBへの接続情報
      logger: loggingのlogger
      read_only:  読み込み用のトランザクション: true(初期値) 登録用のトランザクション: false
      schema: schemaを指定することでトランザクションのスキーマを変更

      使用例)
      ・DBからのデータ取得の場合
      with Transaction(connector, true) as tx
        results = tx.find_all(query)

      ・DBへのデータ登録の場合
      with Transaction(connector, false) as tx
        tx.save(query)

      ・DBからデータを削除の場合
      with Transaction(connector, false) as tx
        tx.delete(query)
  """
  def __init__(self, connector, logger, read_only=True, schema=None):
    self.__connector = connector
    self.__read_only = read_only
    self.__schema = schema
    self.__logger = logger

  def open(self):
    """ トランザクションを開始する
    """
    self.__connect = self.__connector.get_connect()

  def close(self, success_flg=True):
    """ トランザクションを終了する
        読み込みモードの場合は処理が成功したか否かでトランザクションをコミットするかロールバックするかを分ける
        success_flg: 処理成功の場合: true(初期値) 処理失敗の場合はfalse
    """
    if not self.__read_only:
      if success_flg:
        self.__connect.commit()
      else:
        self.__connect.rollback()
    self.__connect.close()

  def find_all(self, query, vars=None):
    """ 全件取得
    """
    self.__logger.debug(f'sql: {query}')
    self.__logger.debug(f'vars: {vars}')
    with self.__connect.cursor(cursor_factory=DictCursor) as cur:
      cur.execute(query, vars)
      result = cur.fetchall()
      self.__logger.debug(f'result: {result}')
      return result

  def find_one(self, query, vars=None):
    """ 1件取得
    """
    self.__logger.debug(f'sql: {query}')
    self.__logger.debug(f'vars: {vars}')
    with self.__connect.cursor(cursor_factory=DictCursor) as cur:
      cur.execute(query, vars)
      result = cur.fetchone()
      self.__logger.debug(f'result: {result}')
      return result

  def save(self, query, vars=None):
    """ 保存処理
    """
    self.__logger.info(f'sql: {query}')
    self.__logger.info(f'vars: {vars}')
    with self.__connect.cursor() as cur:
      cur.execute(query, vars)

  def delete(self, query, vars=None):
    """ 削除処理
    """
    self.__logger.info(f'sql: {query}')
    self.__logger.info(f'vars: {vars}')
    with self.__connect.cursor() as cur:
      cur.execute(query, vars)

  def change_schema(self, schema_name):
    """ スキーマの変更
    """
    self.__logger.info(f'schema_name: {schema_name}')
    with self.__connect.cursor() as cur:
      cur.execute(f'SET search_path TO {schema_name},public;')

  def __enter__(self):
    self.open()
    if self.__schema is not None:
      self.change_schema(self.__schema)
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    if exc_type is not None:
      self.__logger.error(f'エラーの種類: {exc_type}')
      self.__logger.error(f'エラーの値: {exc_value}')
      self.__logger.error(traceback)
    self.close(exc_type is None)
