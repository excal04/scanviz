"""
forms.py: webforms for scanviz web app
author: Jeff
date: 10/2016
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length

class ScanForm(FlaskForm):
    textup = TextAreaField('text upload', validators=[Length(min=0, max=1000)])
    fileup = FileField('scan file (json)')
