from datetime import datetime
from flask import render_template
from GalaxyNV import app

#Globals
#Directories
network_dir="./GalaxyNV/templates/NetworkFiles"
yml_dir=network_dir+"/yml"
json_dir=network_dir+"/json"

#Files
network_json_file=json_dir+"/network.json"
d3_json_file=json_dir+"/d3.json"
d3bridge_json_file=json_dir+"/d3bridge.json"
network_yml_file=yml_dir+"/network.yml"