from datetime import datetime
from flask import request, render_template
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

def createfolders():
    try:
        os.mkdir(network_dir)
        os.mkdir(yml_dir)
        os.mkdir(json_dir)

    except:
        print("Necessary folders already exists. Proceeding.")

def loadfiles():
    try:
        with open(network_yml_file) as networkfile:
            network_list = yaml.load(networkfile, Loader=yaml.FullLoader)

        return (network_list)
    except:
        return("Failed to open network.yml file. Are you sure it is named correctly?")

def convert():
    try:
        with open(network_yml_file) as yaml_in, open(network_json_file, "w") as json_out:
            yaml_object = yaml.safe_load(yaml_in) # yaml_object will be a list or a dict
            json.dump(yaml_object, json_out, indent=4, sort_keys=True)
    except:
        print("Error: Failed to convert yml to json.")

def loadjsonfiles():
    try:
        with open(network_json_file, 'r') as networkfile:
            data = networkfile.read()
            parsed = json.loads(data)
            return json2html.convert(json = parsed)
    except:
        return("Fafiled to open network.json file. Are you sure it is named correctly?")


def graph():
    #Create an empty new dict
    d = { 'nodes': [], 'links': []}

    #Setting the size of the graph
    net = Network('500px', '1000px')#HxW

    #Open the network.json file and begin to parse it
    try:
        with open(network_json_file, 'r') as networkfile:
            parsed = json.loads(networkfile.read())

            #Create empty node list
            nodes = []

            #Add all links and nodes to the nodes list
            for n in parsed["nodes"]:
                if n != "control-br":
                    nodes.append(n)
            for n in parsed["links"]:
                if n != "control-br":
                    nodes.append(n)
    except:
        return ('failed to access json file')

    #Begin to iterate through the nodes list and create the nodes on the graph
    for node in parsed["links"]:
        #Check to make sure that the control-br is NOT being used
        if node != "control-br":
            net.add_node(node, label=node, shape='image', image=r'img_server', size=25)


    for node in parsed["nodes"]:
        #Check to make sure that the control-br is NOT being used
        if node != "control-br":
            #Add the firewall image to the node
            if "-fw" in node:
                net.add_node(node, label=node, shape='image', image=r'img_firewall', size=25)
            if "-https" in node:
                net.add_node(node, label=node, shape='image', image=r'img_security', size=25)
            if "-http" in node:
                net.add_node(node, label=node, shape='image', image=r'img_database', size=25)
            if "admin" in node:
                net.add_node(node, label=node, shape='image', image=r'img_computer', size=25)
            else:
                net.add_node(node, label=node, shape='image', image=r'img_laptop', size=25)

            for link in parsed["nodes"][node]["links"]:
                if(link in nodes):
                    net.add_edge(node, link)

    #Iterate through the nodes again and add any replicas and replica links
    for node in parsed["nodes"]:
        if node != "control-br":
            try:
                replica_count = parsed["nodes"][node]["replicas"]
                
                for r in range(0, replica_count):
                    rep_label = node+'_'+str(r)
                    net.add_node(rep_label, label=rep_label, shape='image', image=r'img_laptop', size=15)

                    for link in parsed["nodes"][node]["links"]:
                        if(link in nodes):
                            net.add_edge(rep_label, link)
            except:
                replica_count = 0

    net.show_buttons()
    net.save_graph(r'GalaxyNV\templates\PyvisGraph.html')
    return ("success")


def create_d3json():
    #Create an empty new dict
    d = { 'nodes': [], 'links': []}
    try:
        #Create the network.json file
        with open(network_json_file, 'r') as networkfile:
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

            with open (d3_json_file, "w") as d3_json_out:
                json.dump(d, d3_json_out, indent=4, sort_keys=False)

            return "Build success."
    except:
        return ("Failed to open network.json file. Are you sure it is named correctly?")

def create_d3jsonbridge():
    #Create an empty new dict
    d = { 'nodes': [], 'links': []}
    try:
        #Create the network.json file
        with open(network_json_file, 'r') as networkfile:
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

            with open (d3bridge_json_file, "w") as d3_json_out:
                json.dump(d, d3_json_out, indent=4, sort_keys=False)

            return "Build success."
    except:
        return ("Failed to open network.json file. Are you sure it is named correctly?")

def add_node(node_name, node_link, image_name, number_of_nodes):
    if request.method=="POST":
        d={ 'nodes': {
            node_name:{
                'image':image_name,
                'type':'lxd',
                'priority':0,
                'links':{
                    node_link:{}},
                'agents':['drone']}}}

        with open(yml_dir+'/data.yml', 'w') as outfile:
            yaml.dump(d, outfile, default_flow_style=False, sort_keys=False)