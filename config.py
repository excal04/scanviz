"""
config.py: configurations for scanviz web app
author: Jeff
date: 10/2016
"""

import os

# these 2 lines used by flask_wtf
WTF_CSRF_ENABLED = True
SECRET_KEY = os.urandom(50)

ELASTIC_SCAN_INDEX = 'dfir'
ELASTIC_SCAN_DOC_TYPE = 'scan'

# configuration of upload location
UPLOAD_LOC = 'uploads/'
