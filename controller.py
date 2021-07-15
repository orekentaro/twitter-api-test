from flask import Flask
from route.main_route import main_route
from common.middleware import before_request
from datetime import timedelta


app = Flask(__name__)
app.secret_key = 'hogehoge'  # セッションが動かなかったんで仮で置きました。

app.register_blueprint(main_route)
app.permanent_session_lifetime = timedelta(minutes=120)
app.before_request(before_request)

if __name__ == '__main__':
  app.debug = True
  app.run(host='127.0.0.1', port=5000)
