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
from ic.logger import logger
from ic.models import *
from ic.forms import *
import ic.handler as Handler
import ic.filters as Filters
import ic.project as Project
import ic.tools as Tools
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Or use any other random string
app.jinja_env.filters['dhaka_time'] = Filters.format_datetime_to_dhaka
app.config['WTF_CSRF_SECRET_KEY'] = os.urandom(24)
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
UPLOAD_FOLDER = 'static' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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

@app.route("/")
def home():
    allProjects = Projects.query.filter_by(projectStatus="Active").all()
    return render_template('index.html', allProjects=allProjects)
@app.route("/project/create", methods=["GET", "POST"])
def projectCreate():
    return Handler.projectCreator(db, request, session)
@app.route("/project/manage", methods=["GET"])
def projectManage():
    return Handler.projectManager(db, request, session)
@app.route("/project/management")
def projectManagement():
    return Handler.projectManagement(db, request, session)
@app.route("/project/<int:projectId>")
def projectView(projectId : int):
    return Project.projectViewer(db, request, session, projectId=projectId)

@app.route("/project/updateClassification/<string:projectCode>", methods=["GET", "POST"])
def classficationUpdate(projectCode : str):
    return Project.classificationUpdater(db, request, session, projectCode=projectCode)


@app.route('/uploadPhotos/<string:projectCode>', methods=['POST'])
def uploadPhotos(projectCode : str):
   return Project.uploadImages(db, request, session, projectCode)


@app.route("/tools")
def toolsView():
    return Tools.toolsViewer(db, request, session)

@app.route("/tool/face-extractor")
def toolFaceExtractorView():
    return Tools.faceExtractorViewer(db, request, session)

@app.route("/upload_video", methods=["GET", "POST"])
def faceExtractorUploader():
    return Tools.faceExtractorUploader(db, request, session)
@app.route('/download/<filename>')
def download_zip(filename):
    return Tools.download_zip(filename)
if __name__ == "__main__":
    app.run(debug=True, port=8989, host="localhost")
    