from flask import render_template, abort, redirect, url_for, flash
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
        print(project_classes)
        print(request.form)
        
        project_classes = [cls.strip() for cls in project_classes if cls.strip()]
        print(project_classes)
        new_project = Projects(
            projectName=project_name,
            projectDescription=project_description,
            projectFolder=project_folder,
            projectClasses=json.dumps(project_classes),
            projectCreatedAt=datetime.now(),
            projectUpdatedAt=datetime.now()
        )
        try:
            db.session.add(new_project)
            db.session.commit()
            flash("Project created successfully", "success")
        except Exception as error:
            logger.error(error)
            db.session.rollback()
            flash("Project creation failed", "error")
        finally:
            db.session.close()
        return redirect(url_for('projectCreate'))  
    else:
        
        return render_template('projectCreate.html', form=form)
    return render_template('projectCreate.html', form=form)
def projectManager(db, request, session):
    projectId = request.args.get("projectId", None)
    projectOperation = request.args.get('operation', None)
    
    print(projectId, projectOperation)
    if projectId and projectOperation:
        projectInfo = Projects.query.filter_by(id = projectId).first()
        if projectInfo is None:
            flash("Project not found", 'warning')
        if projectOperation == "delete":
            try:
                db.session.delete(projectInfo)
                db.session.commit()        
                flash("Project Deleted", "success")
            except Exception as error:
                logger.error(error)
                db.session.rollback()
                flash("Something went wrong","error")

        return redirect(url_for("projectManagement"))
    
    else:
        return "Invalid arguments"
def projectManagement(db, request, session):
    projects = Projects.query.all()
    return render_template("projectManagement.html", projects = projects)