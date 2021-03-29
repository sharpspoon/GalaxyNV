"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import GalaxyNV.views
import GalaxyNV.gnx
import GalaxyNV.networkfiles

#This fixes the iframe loading issue
app.templates_auto_reload=True

networkfiles.createfolders()
networkfiles.loadfiles()
networkfiles.convert()