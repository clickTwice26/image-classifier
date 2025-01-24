from flask import Flask, render_template
from ic.models import Projects
def projectViewer(db, request, session, projectId):
    projectInfo = Project.query.filter_by(id = projectId).first()
    unclassifiedImages = os.listdir(f'static/{projectInfo.projectFolder}')    
    return render_template("project.html", projectInfo = projectInfo, unclassifiedImages = unclassifiedImages)


