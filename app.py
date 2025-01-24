from flask import Flask, render_template, abort, session, redirect, url_for, flash, send_from_directory, request, jsonify
import redis
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import pytz
from flask_caching import Cache
from rq import Queue
from datetime import timedelta, datetime

from ic.models import *
app = Flask(__name__)
app.config['SECRET_KEY'] = "adkasdkljaskldjklajdklajsdkljaklsdjasd"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///ic.db"
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
cache = Cache(app)
redis_connection = redis.Redis(host='localhost', port=6379, db=0)
app.permanent_session_lifetime = timedelta(minutes=30)
db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)
app.app_context().push()
queues = {
    'high': Queue('high', connection=redis_connection),
    'default': Queue('default', connection=redis_connection),
    'low': Queue('low', connection=redis_connection),
}

def getSessionUsername():
    return session.get("username")

limiter = Limiter(
    key_func=getSessionUsername,
    app=app,
    storage_uri="redis://localhost:6379"
)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=8989, host="localhost")