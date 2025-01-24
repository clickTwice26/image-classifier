from flask import Flask, render_template, redirect, flash, url_for, jsonify
from ic.models import Projects
import os
from ic.logger import logger
import shutil

def projectViewer(db, request, session, projectId):
    projectInfo = Projects.query.filter_by(id = projectId).first()
    if projectInfo is None:
        flash('Project not found', "error")
        return redirect(url_for('projectManagement'))
    projectStat = ProjectStats(projectInfo.projectCode)
    unclassifiedImages = os.listdir(os.path.join('static', projectInfo.projectFolder))
    print(unclassifiedImages)
    return render_template("project.html", projectInfo = projectInfo, unclassifiedImages = unclassifiedImages, projectStat = projectStat)


import os
from pathlib import Path

class ProjectStats:
    def __init__(self, projectCode: str):
        try:
            self.projectInfo = Projects.query.filter_by(projectCode=projectCode).first()
            if not self.projectInfo:
                raise ValueError(f"Project with code {projectCode} not found.")
            self.getClassifiedNumber()
        except Exception as e:
            print(f"Error initializing ProjectStats: {e}")

    def getClassifiedNumber(self):
        try:
            project_folder_path = Path("static") / self.projectInfo.projectFolder
            self.unclassifiedNumber = len(list(project_folder_path.glob('*')))

            self.classifiedNumber = 0
            self.disqualifiedNumber = 0
            classified_folder_path = Path("static") / "classified_images"
            classifiedImages = []

            for image in classified_folder_path.iterdir():
                if image.name.startswith(f"classified_{self.projectInfo.projectCode}"):
                    classifiedImages.append(image)

            self.classifiedNumber = len(classifiedImages)
        except Exception as e:
            print(f"Error while calculating classified numbers: {e}")



def classificationUpdater(db, request, session, projectCode):
    try:
        data = request.get_json()
        classifications = data.get('classifications', {})
        disqualified = data.get('disqualified', [])
        
        projectInfo = Projects.query.filter_by(projectCode=projectCode).first()
        if not projectInfo:
            return jsonify({"message": "Project not found"}), 404

        source_dir = os.path.join("static", projectInfo.projectFolder)
        classified_dir = os.path.join("static", "classified_images")
        
        os.makedirs(classified_dir, exist_ok=True)

        for class_name, images in classifications.items():
            for image in images:
                source_path = os.path.join(source_dir, image)
                dest_path = os.path.join(classified_dir, f"classified_{projectInfo.projectCode}_{class_name}_{image}")

                if os.path.exists(source_path):
                    try:
                        shutil.move(source_path, dest_path)
                        logger.info(f"Moved image {image} to {dest_path}")
                    except Exception as e:
                        logger.error(f"Failed to move {image}: {str(e)}")
                else:
                    logger.warning(f"Image {image} not found in {source_dir}")

        for image in disqualified:
            source_path = os.path.join(source_dir, image)
            if os.path.exists(source_path):
                logger.info(f"Image {image} marked as disqualified.")
            else:
                logger.warning(f"Disqualified image {image} not found in {source_dir}")
        
        logger.info(f"Classification update data: {data}")

        return jsonify({"message": "Classification update successful!"}), 200

    except Exception as e:
        logger.error(f"Error in classificationUpdater: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
