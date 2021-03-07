from datetime import datetime
from flask import render_template
from GalaxyNV import app
from json2html import *
import networkx as nx
import matplotlib.pyplot as plt
import os
import yaml
import json
import pprint
from collections import defaultdict

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
            json.dump(yaml_object, json_out, indent=4, sort_keys=True)
    except:
        print("Error: Failed to convert yml to json.")

def loadjsonfiles():
    try:
        with open(r'GalaxyNV\templates\network.json', 'r') as networkfile:
            data = networkfile.read()
            parsed = json.loads(data)
            return json2html.convert(json = parsed)
    except:
        return("Failed to open network.json file. Are you sure it is named correctly?")



d = { 'nodes': [], 'links': []}

def create_d3json():
    try:
        with open(r'GalaxyNV\templates\network.json', 'r') as networkfile:
            data = networkfile.read()
            parsed = json.loads(data)
            value = []
            for item in parsed["nodes"]:
                value.append(item)

                d['nodes'].append({'id':item, 'group':1})

                for l in parsed["nodes"][item]["links"]:
                    d['links'].append({'source':item, 'target':l, 'value':1})

            with open (r'GalaxyNV\templates\fdg.json', "w") as fdg_json_out:
                json.dump(d, fdg_json_out, indent=4, sort_keys=False)

            return d
    except:
        return ("Failed to open network.json file. Are you sure it is named correctly?")

