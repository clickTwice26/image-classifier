import os
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

from ic.programs import getEmptyDirectorys
class ProjectForm(FlaskForm):
    projectName = StringField('Project Name', validators=[DataRequired()])
    projectDescription = TextAreaField('Project Description', validators=[DataRequired()])
    # projectFolder = SelectField('Project Folder', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Create Project')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        
    #     emptyFolders = getEmptyDirectorys('static')  # Use your function here
    #     self.projectFolder.choices = [('', 'Select a Folder')] + [(folder, folder) for folder in emptyFolders]
