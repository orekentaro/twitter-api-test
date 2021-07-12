from flask import render_template
from models.base_model import BaseModel

class MainModel(BaseModel):
  def main_page(self):
    return render_template('main.html')
