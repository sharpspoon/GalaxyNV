"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import GalaxyNV.views
import GalaxyNV.networkfiles

#This fixes the iframe loading issue
app.templates_auto_reload=True

networkfiles.createfolders()
networkfiles.convert()
networkfiles.create_test_nodes()
networkfiles.image_list()