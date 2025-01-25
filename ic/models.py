import json
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from flask import flash
db = SQLAlchemy()
import random
import string

def getUniqueToken(length=5) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projectName = db.Column(db.String(100), nullable=False)
    projectDescription = db.Column(db.String(500), nullable=False)
    projectFolder = db.Column(db.String(100), nullable=False)
    projectStatus = db.Column(db.String(100), nullable=False, default="Active")
    projectCreatedAt = db.Column(db.DateTime, default=datetime.now)
    projectUpdatedAt = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    projectClasses = db.Column(db.Text, nullable=True, default="[]")
    projectCode = db.Column(db.String(200), nullable=False, default=getUniqueToken())
    
    
    def getProjectClasses(self) -> list:
        return json.loads(self.projectClasses)
    def addProjectClass(self, className : str) -> list:
        classes = self.getProjectClasses()
        classes = list(set(classes.append(className)))
        self.projectClasses = json.dumps(classes)
        return classes 
    def removeProjectClass(self, className : str) -> list:
        classes = self.getProjectClasses()
        classes = list(set(classes.remove(className)))
        self.projectClasses = json.dumps(classes)
        return classes