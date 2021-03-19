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
from pyvis.network import Network


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


def graph():
    #Create an empty new dict
    d = { 'nodes': [], 'links': []}

    net = Network('500px', '1000px')#HxW
    try:
        with open(r'GalaxyNV\templates\network.json', 'r') as networkfile:
            parsed = json.loads(networkfile.read())
            nodes = []

            for n in parsed["nodes"]:
                if n != "control-br":
                    nodes.append(n)
            for n in parsed["links"]:
                if n != "control-br":
                    nodes.append(n)
    except:
        return ('failed to access json file')


    #nx_graph = nx.cycle_graph(3)
    id = 0
    for node in parsed["links"]:
        if node != "control-br":
            id+=1
            net.add_node(node, label=node, shape='image', image=r'img_laptop', size=25)

    for node in parsed["nodes"]:
        if node != "control-br":
            id+=1
            net.add_node(node, label=node, shape='image', image=r'img_server', size=25)
            for link in parsed["nodes"][node]["links"]:
                if(link in nodes):
                    net.add_edge(node, link)

    net.show_buttons()
    net.save_graph(r'GalaxyNV\templates\PyvisGraph.html')
    return ("success")


def create_d3json():
    #Create an empty new dict
    d = { 'nodes': [], 'links': []}
    try:
        #Create the network.json file
        with open(r'GalaxyNV\templates\network.json', 'r') as networkfile:
            parsed = json.loads(networkfile.read())

            nodes = []
            for n in parsed["nodes"]:
                if n != "control-br":
                    nodes.append(n)
            for n in parsed["links"]:
                if n != "control-br":
                    nodes.append(n)

            for node in parsed["links"]:
                if node != "control-br":
                    d['nodes'].append({'id':node, 'group':1})

            for node in parsed["nodes"]:
                d['nodes'].append({'id':node, 'group':2})

                for link in parsed["nodes"][node]["links"]:
                    if(link in nodes):
                        d['links'].append({'source':node, 'target':link, 'value':1})

            with open (r'GalaxyNV\templates\fdg.json', "w") as fdg_json_out:
                json.dump(d, fdg_json_out, indent=4, sort_keys=False)

            return "Build success."
    except:
        return ("Failed to open network.json file. Are you sure it is named correctly?")

def create_d3jsonbridge():
    #Create an empty new dict
    d = { 'nodes': [], 'links': []}
    try:
        #Create the network.json file
        with open(r'GalaxyNV\templates\network.json', 'r') as networkfile:
            parsed = json.loads(networkfile.read())

            nodes = []
            for n in parsed["nodes"]:
                nodes.append(n)
            for n in parsed["links"]:
                nodes.append(n)

            for node in parsed["links"]:
                d['nodes'].append({'id':node, 'group':1})

            for node in parsed["nodes"]:
                d['nodes'].append({'id':node, 'group':2})

                for link in parsed["nodes"][node]["links"]:
                    if(link in nodes):
                        d['links'].append({'source':node, 'target':link, 'value':1})

            with open (r'GalaxyNV\templates\fdgbridge.json', "w") as fdg_json_out:
                json.dump(d, fdg_json_out, indent=4, sort_keys=False)

            return "Build success."
    except:
        return ("Failed to open network.json file. Are you sure it is named correctly?")

