from datetime import datetime
from flask import render_template
from GalaxyNV import app
import networkx as nx
import matplotlib.pyplot as plt

def a():
    G = nx.petersen_graph()
    #plt.subplot(121)
    #plt.show()
    nx.draw(G, with_labels=True, font_weight='bold')

def b():
    G = nx.graph
    G.add_node(1)
    G.add_nodes_from([2, 3])
    return (G)