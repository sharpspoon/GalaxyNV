from datetime import datetime
from flask import render_template
from GalaxyNV import app
import networkx as nx
import matplotlib.pyplot as plt
import os
import yaml
import json

def createfolders():
    try:
        os.mkdir("./NetworkYMLFiles")
    except:
        print("Folder 'NetworkYMLFiles' already exists. Proceeding.")

def loadfiles():
    try:
        with open(r'NetworkYMLFiles\network.yml') as networkfile:
            network_list = yaml.load(networkfile, Loader=yaml.FullLoader)

        return (network_list)
    except:
        return("Failed to open network.yml file. Are you sure it is named correctly?")

def convert():
    try:
        with open(r'NetworkYMLFiles\network.yml') as yaml_in, open(r'GalaxyNV\templates\network.json', "w") as json_out:
            yaml_object = yaml.safe_load(yaml_in) # yaml_object will be a list or a dict
            json.dump(yaml_object, json_out)
    except:
        print("Error: Failed to convert yml to json.")

def loadjsonfiles():
    try:
        with open(r'GalaxyNV\templates\network.json', "w") as networkfile:
            network_list = yaml.load(networkfile, Loader=yaml.FullLoader)

        return (json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4))
    except:
        return("Failed to open network.json file. Are you sure it is named correctly?")