"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import GalaxyNV.views
import GalaxyNV.gnx
import GalaxyNV.networkfiles

networkfiles.createfolders()
networkfiles.loadfiles()
networkfiles.convert()