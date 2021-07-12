from flask import render_template
from models.base_model import BaseModel

class MainModel(BaseModel):
  def top_page(self):
    return render_template('main/top_page.html')

  def user_search(self):
    return render_template('main/user_search.html')

  def tweet_search(self):
    return render_template('main/tweet_search.html')

  def tweet_out(self):
    return render_template('main/tweet_out.html')