import logging.config
from common.db import DbConnecter
from common.config import get_config
from common.db import Transaction


class BaseModel():
  def __init__(self):
    # コンフィグファイル読み込み
    self._config = get_config()

    # ログの設定を行う
    logging.config.dictConfig(self._config['log'])
    self._logger = logging.getLogger("app_logger")

    # DBの設定
    db_info = self._config['database']
    self._connector = DbConnecter(
      db_info['dbname'],
      db_info['host'],
      db_info['user'],
      db_info['password']
    )

  def start_transaction(self, read_only=False):
    # 現時点ではスキーマはべた書き(大学追加時に再度考慮する)
    return Transaction(self._connector, self._logger, read_only, 'sagami')

  def get_config_value(self, key):
    """ 大学ごと設定値の取得処理

    Args:
        key (string): 大学ごと設定値のkey

    Raises:
        Exception: keyに紐付く大学ごと設定値が取得できない場合はエラー

    Returns:
        string: keyに紐付く大学ごとの設定値
    """
    self._logger.debug(f'key: {key}')
    with self.start_transaction() as tx:

      sql = "SELECT value FROM config  WHERE key = %s"
      result = tx.find_one(sql, [key])

    if result is None:
      self._logger.error(f'keyに紐付く大学ごと設定値が取得できません。 key: {key}')
      raise Exception()

    self._logger.debug(f'result: {result}')
    return result["value"]
