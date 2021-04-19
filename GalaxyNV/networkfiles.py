from datetime import datetime
from flask import request, render_template
from GalaxyNV import app, globals, views
from json2html import *
import networkx as nx
import matplotlib.pyplot as plt
import os
import yaml
import json
import pprint
from collections import defaultdict
from pyvis.network import Network
import hiyapyco

def createfolders():
    try:
        #os.mkdir(globals.network_dir)
        #os.mkdir(globals.yml_dir)
        #os.mkdir(globals.json_dir)
        #os.mkdir(globals.system_dir)
        os.mkdir(globals.image_nodes_dir)
    except:
        print("Necessary folders already exists. Proceeding.")

def create_test_nodes():
    try:
        os.mkdir(globals.image_nodes_dir+"/admin-fw")
        os.mkdir(globals.image_nodes_dir+"/admin0")
        os.mkdir(globals.image_nodes_dir+"/border-fw")
        os.mkdir(globals.image_nodes_dir+"/server-fw")
        os.mkdir(globals.image_nodes_dir+"/server-http")
        os.mkdir(globals.image_nodes_dir+"/server-https")
        os.mkdir(globals.image_nodes_dir+"/user-fw")
        os.mkdir(globals.image_nodes_dir+"/user0")
        os.mkdir(globals.image_nodes_dir+"/user1")
        os.mkdir(globals.image_nodes_dir+"/user200")
    except:
        print("all exist")

def loadfiles():
    try:
        with open(globals.network_yml_file) as networkfile:
            network_list = yaml.load(networkfile, Loader=yaml.FullLoader)

        return (network_list)
    except:
        return("Failed to open network.yml file. Are you sure it is named correctly?")

def convert():
    try:
        with open(globals.network_yml_file) as yaml_in, open(globals.network_json_file, "w") as json_out:
            yaml_object = yaml.safe_load(yaml_in) # yaml_object will be a list or a dict
            json.dump(yaml_object, json_out, indent=4, sort_keys=True)
    except:
        print("Error: Failed to convert yml to json.")

def loadjsonfiles():
    try:
        with open(globals.network_json_file, 'r') as networkfile:
            data = networkfile.read()
            parsed = json.loads(data)
            return json2html.convert(json = parsed)
    except:
        return("Failed to open network.json file. Are you sure it is named correctly?")


def graph():
    #Create an empty new dict
    d = { 'nodes': [], 'links': []}

    #Setting the size of the graph
    net = Network('500px', '1000px')#HxW

    #Open the network.json file and begin to parse it
    try:
        with open(globals.network_json_file, 'r') as networkfile:
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
    
    return net.save_graph(r'GalaxyNV\templates\PyvisGraph.html')


def create_d3json():
    #Create an empty new dict
    d = { 'nodes': [], 'links': []}
    try:
        #Create the network.json file
        with open(globals.network_json_file, 'r') as networkfile:
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
        if node_link:
            d={ 'nodes': {
                node_name:{
                    'image':image_name,
                    'type':'lxd',
                    'priority':0,
                    'links':{
                        node_link:{}},
                    'agents':['drone'],
                    'replicas':int(number_of_nodes)}}}
        else:
            d={ 'nodes': {
                node_name:{
                    'image':image_name,
                    'type':'lxd',
                    'priority':0,
                    'links':{},
                    'agents':['drone'],
                    'replicas':int(number_of_nodes)}}}

        with open(globals.yml_dir+'/newnode.yml', 'w') as outfile:
            yaml.dump(d, outfile, default_flow_style=False, sort_keys=False)

        with open(globals.network_yml_file) as networkfile:
            data1 = yaml.load(networkfile, Loader=yaml.FullLoader)

        with open(globals.yml_dir+'/newnode.yml') as newnode:
            data2 = yaml.load(newnode, Loader=yaml.FullLoader)

        conf = hiyapyco.load(globals.network_yml_file, globals.yml_dir+'/newnode.yml', method=hiyapyco.METHOD_MERGE, interpolate=True, failonmissingfiles=True, usedefaultyamlloader=True)

        with open(globals.network_yml_file, 'w') as outfile:
            yaml.dump(conf, outfile, default_flow_style=False, sort_keys=False)

        loadfiles()
    return convert()

def remove_node(node_name):
    if request.method=="POST":

        with open(globals.network_yml_file) as networkfile:
            data1 = yaml.load(networkfile, Loader=yaml.FullLoader)

        del data1['nodes'][node_name]

        with open(globals.network_yml_file, 'w') as outfile:
            yaml.dump(data1, outfile, default_flow_style=False, sort_keys=False)

        loadfiles()
    return convert()

def link_list():
    with open(globals.network_yml_file) as networkfile:
        data1 = yaml.load(networkfile, Loader=yaml.FullLoader)

    link_list=""
    for n in data1["nodes"]:
        link_list+='''<option value="'''+n+'''">'''+n+'''</option>'''
    return link_list

def image_list():
    image_list=""
    #print (os.listdir(globals.image_nodes_dir))
    for folder in (os.listdir(globals.image_nodes_dir)):
        image_list+='''<option value="'''+folder+'''">'''+folder+'''</option>'''
    return image_list

def build_add_link_page_scripts():
    try:
        with open(globals.network_yml_file) as networkfile:
            data1 = yaml.load(networkfile, Loader=yaml.FullLoader)


        script='''<script>'''
        for n in data1["nodes"]:
            #Check if there is a '-' in the node name. If there is, remove it for the javascript function.
            
            if "-" in n:
                n2=n.replace('-', '')
                script+='''function addLinkTo_'''+n2+'''Function() {document.getElementById("jsAddLinkTo_'''+n2+'''").innerHTML = '<select class="form-select" aria-label="Default select example">'''+link_list()+'''</select>';}'''
            else:
                script+='''function addLinkTo_'''+n+'''Function() {document.getElementById("jsAddLinkTo_'''+n+'''").innerHTML = '<select class="form-select" aria-label="Default select example">'''+link_list()+'''</select>';}'''
        script+='''</script>'''
        return script
    except:
        return ("Failed to open network.json file. Are you sure it is named correctly?")

def load_nodes_to_edit():
    try:
        with open(globals.network_yml_file) as networkfile:
            data1 = yaml.load(networkfile, Loader=yaml.FullLoader)

            nodes = ""
            for n in data1["nodes"]:
                links=""
                try:
                    replicas=data1["nodes"][n]["replicas"]
                except:
                    replicas=0
                #Check if there is a '-' in the node name. If there is, remove it for the javascript function.
                if "-" in n:
                    n2=n.replace('-', '')
                    links+='''<div id="jsAddLinkTo_'''+n2+'''"></div>'''
                else:
                    links+='''<div id="jsAddLinkTo_'''+n+'''"></div>'''
                
                if data1["nodes"][n]["links"] != {}:

                    links+='<table>'
                    for l in data1["nodes"][n]["links"]:
                        links+=(r'''<tr><td><select class="form-select" aria-label="Default select example"><option selected>'''+str(l)+'''</option>'''+link_list()+'''</select></td><td><input type="checkbox" class="btn-check form-control" id="id_delete_'''+n+'''_'''+str(l)+'''" name="delete_'''+n+'''_'''+str(l)+'''" autocomplete="off"><label class="btn btn-outline-danger" for="id_delete_'''+n+'''_'''+str(l)+'''">X</label></td></tr>''')
                    links+='</table>'

                #Check if there is a '-' in the node name. If there is, remove it for the javascript function.
                if "-" in n:
                    n2=n.replace('-', '')
                    links+='''<button type="button" class="btn btn-outline-success btn-sm" id="id_addLinkTo_'''+n+'''" name="addLinkTo_'''+n+'''" data-bs-toggle="tooltip" data-bs-placement="top" title="Add link to '''+n+'''" onclick="addLinkTo_'''+n2+'''Function()">Add Link</button>'''
                else:
                    links+='''<button type="button" class="btn btn-outline-success btn-sm" id="id_addLinkTo_'''+n+'''" name="addLinkTo_'''+n+'''" data-bs-toggle="tooltip" data-bs-placement="top" title="Add link to '''+n+'''" onclick="addLinkTo_'''+n+'''Function()">Add Link</button>'''
                
                nodes+=(r'''<tr><th scope="row"><input type="text" class="form-control" id="nodeNameId" name="'''+n+'''" aria-describedby="nodeHelp" value="'''+str(n)+r'''" required></th><td>'''+str(links)+r'''</td><td><input type="number" class="form-control" id="numberOfNodesId" name="replicas_'''+str(n)+'''" value="'''+str(replicas)+'''"></td><td><input type="checkbox" class="btn-check form-control" id="id_delete_'''+n+'''" name="delete_'''+n+'''" autocomplete="off""><label class="btn btn-outline-danger" for="id_delete_'''+n+'''">X</label></td></tr>''')
            return nodes
    except:
        return ("Failed to open network.json file. Are you sure it is named correctly?")

def change_node_name(n, new_node_name):
    #if request.method=="GET":

    with open(globals.network_yml_file) as networkfile:
        data1 = yaml.load(networkfile, Loader=yaml.FullLoader)

    data1["nodes"][new_node_name]=data1["nodes"][n]
    del data1["nodes"][n]

    with open(globals.network_yml_file, 'w') as outfile:
        yaml.dump(data1, outfile, default_flow_style=False, sort_keys=False)

    loadfiles()
    return convert()

def change_node_replicas(n, current_node_replicas, new_node_replicas):
    #if request.method=="GET":

    with open(globals.network_yml_file) as networkfile:
        data1 = yaml.load(networkfile, Loader=yaml.FullLoader)

    data1["nodes"][n]["replicas"]=new_node_replicas

    with open(globals.network_yml_file, 'w') as outfile:
        yaml.dump(data1, outfile, default_flow_style=False, sort_keys=False)

    loadfiles()
    return convert()

def remove_node_link(node_name, node_link):
    if request.method=="POST":

        with open(globals.network_yml_file) as networkfile:
            data1 = yaml.load(networkfile, Loader=yaml.FullLoader)

        del data1['nodes'][node_name]['links'][node_link]

        with open(globals.network_yml_file, 'w') as outfile:
            yaml.dump(data1, outfile, default_flow_style=False, sort_keys=False)

        loadfiles()
    return convert()