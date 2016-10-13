
from flask import Flask
import os

app = Flask(__name__)
app.config.from_object('config')

# connect to elasticsearch by default connects to localhost:9200
from elasticsearch import Elasticsearch
es = Elasticsearch()

from app import views
