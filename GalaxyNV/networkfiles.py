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

def createfolders():
    try:
        os.mkdir("./NetworkYMLFiles")
    except:
        print("Folder 'NetworkYMLFiles' already exists. Proceeding.")

def loadfiles():
    try:
        with open(r'NetworkYMLFiles\network.yml') as networkfile:
            network_list = yaml.load(networkfile, Loader=yaml.FullLoader)

        return (networkfile)
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
            your_json = '{ "glossary": { "title": "example glossary", "GlossDiv": { "title": "S", "GlossList": { "GlossEntry": { "ID": "SGML", "SortAs": "SGML", "GlossTerm": "Standard Generalized Markup Language", "Acronym": "SGML", "Abbrev": "ISO 8879:1986", "GlossDef": { "para": "A meta-markup language, used to create markup languages such as DocBook.", "GlossSeeAlso": ["GML", "XML"] }, "GlossSee": "markup" } } } } }'
            your_json2 = '{"nodes": {"border-fw": {"image": "border-fw", "type": "lxd", "priority": 0, "links": {"control-br": {}, "dmz-br": {}, "upstream-br": {}}, "agents": ["drone"]}, "user-fw": {"image": "user-fw", "type": "lxd", "priority": 0, "links": {"control-br": {}, "dmz-br": {}, "user0-br": {}, "user1-br": {}, "user200-br": {}}, "agents": ["drone"]}, "server-fw": {"image": "server-fw", "type": "lxd", "priority": 0, "links": {"control-br": {}, "dmz-br": {}, "server0-br": {}}, "agents": ["drone"]}, "admin-fw": {"image": "admin-fw", "type": "lxd", "priority": 0, "links": {"control-br": {}, "dmz-br": {}, "admin0-br": {}}, "agents": ["drone"]}, "admin0": {"image": "admin0", "priority": 60, "type": "lxd", "links": {"control-br": {}, "admin0-br": {}}, "agents": ["admin", "drone"]}, "server-http": {"hostname": "downloadmoreram", "image": "server-http", "type": "lxd", "priority": 70, "links": {"control-br": {}, "server0-br": {}}, "agents": ["drone"]}, "server-https": {"hostname": "downloadmoresecurity", "image": "server-https", "type": "lxd", "priority": 70, "links": {"control-br": {}, "server0-br": {}}, "agents": ["drone"]}, "user0": {"image": "user0", "type": "lxd", "priority": 80, "links": {"control-br": {}, "user0-br": {}}, "agents": ["user", "drone"], "replicas": 3}, "user1": {"image": "user1", "type": "lxd", "priority": 90, "links": {"control-br": {}, "user1-br": {}}, "agents": ["user", "drone"], "replicas": 3}, "user200": {"image": "user200", "type": "lxd", "priority": 100, "links": {"control-br": {}, "user200-br": {}}, "agents": ["user", "drone"], "replicas": 5}}, "links": {"control-br": {"type": "lxd"}, "upstream-br": {"type": "lxd"}, "dmz-br": {"type": "lxd"}, "admin0-br": {"type": "lxd"}, "server0-br": {"type": "lxd"}, "user0-br": {"type": "lxd"}, "user1-br": {"type": "lxd"}, "user200-br": {"type": "lxd"}}}'
            data = networkfile.read()
            parsed = json.loads(data)
            

            return json2html.convert(json = parsed)
    except:
        return("Failed to open network.json file. Are you sure it is named correctly?")