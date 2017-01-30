from flask import Flask
import redis
import os

app = Flask(__name__)
app.config.from_object('config')

app.redis = redis.StrictRedis(host=os.getenv('REDIS_HOST', 'localhost'), port=os.getenv('REDIS_PORT', '6379'), db=0)


from app import views
