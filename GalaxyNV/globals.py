from datetime import datetime
from flask import render_template
from GalaxyNV import app

#Globals
DEBUG=True

#Directories
network_dir="./GalaxyNV/templates/NetworkFiles"
yml_dir=network_dir+"/yml"
json_dir=network_dir+"/json"
system_dir="./GalaxyNV/templates/system"
infrastructure_dir="./GalaxyNV/infrastructure"
image_dir="./GalaxyNV/infrastructure/images"
image_nodes_dir="./GalaxyNV/infrastructure/images/nodes"

#Files
network_json_file=json_dir+"/network.json"
d3_json_file=json_dir+"/d3.json"
d3bridge_json_file=json_dir+"/d3bridge.json"
network_yml_file=yml_dir+"/network.yml"
log_file=system_dir+"/log.json"
history_file=system_dir+"/history.json"