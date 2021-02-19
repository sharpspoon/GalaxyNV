from datetime import datetime
from flask import render_template
from GalaxyNV import app
import networkx as nx
import matplotlib.pyplot as plt

def subheader1():
    return ("Welcome to Galaxy. To get started, upload a network.yml file.")

def b():
    G = nx.graph
    G.add_node(1)
    G.add_nodes_from([2, 3])
    return (G)