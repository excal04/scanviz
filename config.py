
import os

# these 2 lines used by flask_wtf
WTF_CSRF_ENABLED = True
SECRET_KEY = os.urandom(50)
