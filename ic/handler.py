from flask import render_template, abort, redirect, url_for
from ic.forms import ProjectForm
import os
from ic.models import Projects
import json
from datetime import datetime
from ic.logger import logger
def projectCreator(db, request, session):
    form = ProjectForm()
    if form.validate_on_submit():
        project_name = form.projectName.data
        project_description = form.projectDescription.data
        project_folder = form.projectFolder.data
        project_classes = request.form.get('projectClasses', '').split(',')  # Split by commas
        project_classes = [cls.strip() for cls in project_classes if cls.strip()]
        new_project = Projects(
            projectName=project_name,
            projectDescription=project_description,
            projectFolder=project_folder,
            projectClasses=json.dumps(project_classes),
            projectCreatedAt=datetime.now(),
            projectUpdatedAt=datetime.now()
        )
        
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('projectCreate'))  # Redirect to the list of projects or another page
    else:
        
        return render_template('projectCreate.html', form=form)
    return render_template('projectCreate.html', form=form)
def projectManager(db, request, session):
    projectId = request.args.get("projectId", None)
    if projectId is None:
        return redirect(url_for('projectManage'))
    