from flask import Flask
from route.main_route import main_route

app = Flask(__name__)
app.secret_key = 'hogehoge'  # セッションが動かなかったんで仮で置きました。

app.register_blueprint(main_route)

if __name__ == '__main__':
  app.debug = True
  app.run(host='127.0.0.1', port=5000)
