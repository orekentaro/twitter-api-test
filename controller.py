from flask import Flask

app = Flask(__name__)
app.secret_key = 'hogehoge'  # セッションが動かなかったんで仮で置きました。

if __name__ == '__main__':
  app.debug = True
  app.run(host='127.0.0.1', port=5000)
