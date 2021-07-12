from flask import Blueprint
from models.base_model import BaseModel

class MainModel(BaseModel):
  def top_page(self):
    return 'Hello'
