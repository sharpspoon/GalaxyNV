from datetime import datetime
from flask import render_template
from GalaxyNV import app
import networkx as nx
import matplotlib.pyplot as plt
import os
import yaml

def createfolders():
    try:
        os.mkdir("./NetworkYMLFiles")
    except:
        print("Folder 'NetworkYMLFiles' already exists. Proceeding.")

def loadfiles():
    try:
        with open(r'NetworkYMLFiles\network.yml') as networkfile:
            network_list = yaml.load(networkfile, Loader=yaml.FullLoader)
            print(network_list)
            return (network_list)
    except:
        print("Failed to open network.yml file. Are you sure it is named correctly?")
        return("Failed to open network.yml file. Are you sure it is named correctly?")