from datetime import datetime
from flask import Flask, request, render_template, send_file
from GalaxyNV import app, gnx, networkfiles, globals
import yaml

##########
# Images #
##########
@app.route('/img_laptop')
def img_laptop():
    return send_file(
        r'static\img\laptop.png', mimetype='image/png'
    )

@app.route('/img_computer')
def img_computer():
    return send_file(
        r'static\img\computer.png', mimetype='image/png'
    )

@app.route('/img_server')
def img_server():
    return send_file(
        r'static\img\server.png', mimetype='image/png'
    )

@app.route('/img_database')
def img_database():
    return send_file(
        r'static\img\database.png', mimetype='image/png'
    )

@app.route('/img_security')
def img_security():
    return send_file(
        r'static\img\security.png', mimetype='image/png'
    )

@app.route('/img_firewall')
def img_firewall():
    return send_file(
        r'static\img\firewall.png', mimetype='image/png'
    )

#########
# Pages #
#########
@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        sh1=gnx.subheader1(),
        nodes=networkfiles.load_nodes_to_edit(),
        images=networkfiles.image_list(),
        js=networkfiles.build_add_link_page_scripts(),
        links=networkfiles.link_list()
    )

@app.route('/image')
def image():
    return render_template(
        'image.html',
        title='Galaxy Image and Network Configuration',
        year=datetime.now().year,
        nodes=networkfiles.load_nodes_to_edit(),
        images=networkfiles.image_list(),
        js=networkfiles.build_add_link_page_scripts(),
        links=networkfiles.link_list()
    )

@app.route('/contact')
def contact():
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.',
        nodes=networkfiles.load_nodes_to_edit(),
        images=networkfiles.image_list(),
        js=networkfiles.build_add_link_page_scripts(),
        links=networkfiles.link_list()
    )

@app.route('/history')
def history():
    return render_template(
        'history.html',
        title='history',
        year=datetime.now().year,
        nodes=networkfiles.load_nodes_to_edit(),
        images=networkfiles.image_list(),
        js=networkfiles.build_add_link_page_scripts(),
        links=networkfiles.link_list()
    )

@app.route('/networkyaml')
def networkyaml():
    return render_template(
        'networkyaml.html',
        year=datetime.now().year,
        yc = networkfiles.loadfiles(),
        jc = networkfiles.loadjsonfiles(),
        nodes=networkfiles.load_nodes_to_edit(),
        images=networkfiles.image_list(),
        js=networkfiles.build_add_link_page_scripts(),
        links=networkfiles.link_list()
    )

#Pyvis graph html page
@app.route('/graph')
def graph():
    return render_template(
        'graph.html',
        year=datetime.now().year,
        nodes=networkfiles.load_nodes_to_edit(),
        images=networkfiles.image_list(),
        js=networkfiles.build_add_link_page_scripts(),
        links=networkfiles.link_list()
    )

#Force directed graph with no bridge display
@app.route('/fdg')
def fdg():
    return render_template(
        'fdg.html',
        year=datetime.now().year,
        jc = networkfiles.create_d3json(),
        nodes=networkfiles.load_nodes_to_edit(),
        images=networkfiles.image_list(),
        js=networkfiles.build_add_link_page_scripts(),
        links=networkfiles.link_list()
    )

#Force directed graph with a bridge display
@app.route('/fdgbridge')
def fdgbridge():
    return render_template(
        'fdgbridge.html',
        year=datetime.now().year,
        jc = networkfiles.create_d3jsonbridge(),
        nodes=networkfiles.load_nodes_to_edit(),
        images=networkfiles.image_list(),
        js=networkfiles.build_add_link_page_scripts(),
        links=networkfiles.link_list()
    )

###########
# Iframes #
###########
@app.route('/demoiframe')
def demoiframe():
    return render_template(
        'Demo.html'
    )

@app.route('/graphiframe')
def graphiframe():
    #networkfiles.graph()
    return render_template(
        'PyvisGraph.html'
    )

#Force directed graph with no bridge display
@app.route('/fdgiframe')
def fdgiframe():
    return render_template(
        'ForceDirectedGraph.html'
    )

#Force directed graph with a bridge display
@app.route('/fdgbridgeiframe')
def fdgbridgeiframe():
    return render_template(
        'ForceDirectedGraphBridge.html'
    )

##############
# Json Files #
##############
@app.route('/d3json')
def d3json():
    return render_template(
        'NetworkFiles/json/d3.json'
    )

@app.route('/d3jsonbridge')
def d3jsonbridge():
    return render_template(
        'NetworkFiles/json/d3bridge.json'
    )

@app.route('/json')
def json():
    return render_template(
        'network.json'
    )

@app.route('/jsonbridge')
def jsonbridge():
    return render_template(
        'networkbridge.json'
    )

@app.route('/demojson')
def demojson():
    return render_template(
        'NetworkFiles/json/demo.json'
    )

############
# Commands #
############
@app.route('/addnode', methods =["POST"])
def addnode():
    node_name = request.form.get("nodeName")
    node_link = request.form.get("nodeLink")
    image_name = request.form.get("imageName")
    number_of_nodes = request.form.get("numberOfNodes")
    hostname = request.form.get("hostname")
    priority = request.form.get("priority")
    networkfiles.add_node(node_name, node_link, image_name, number_of_nodes, hostname, priority)
    graphiframe()
    networkfiles.load_nodes_to_edit()
    return graph()

@app.route('/editnodes', methods =["POST"])
def editnodes():
    #Get a list of all nodes in the yaml file
    with open(globals.network_yml_file) as networkfile:
        data1 = yaml.load(networkfile, Loader=yaml.FullLoader)

    #Iterate through the list of nodes
    for n in data1["nodes"]:
        #Set each form element value to a var
        new_node_name=request.form.get(n)
        new_node_replicas = request.form.get(n+"_replicas")
        new_node_hostname = request.form.get(n+"_hostname")
        new_node_priority = request.form.get(n+"_priority")
        delete_node_name = request.form.get("delete_"+n)
        try:
            current_node_replicas=data1["nodes"][n]["replicas"]
        except:
            current_node_replicas=0
        try:
            current_node_hostname=data1["nodes"][n]["hostname"]
        except:
            current_node_hostname=""
        try:
            current_node_priority=data1["nodes"][n]["priority"]
        except:
            current_node_priority=0
        

        for l in data1["nodes"][n]["links"]:
            delete_link_name = request.form.get("delete_"+n+"_"+l)
            if delete_link_name:
                if globals.DEBUG==True:
                    print ('Deleting the link: '+n+' ---> '+l)
                networkfiles.remove_node_link(n, l)

            link_name = request.form.get("Link_"+n+"_"+l)
            if link_name != l:
                networkfiles.change_node_link(n, l, link_name)
        try:
            new_node_link=request.form.get("new_"+n+"_link")
        except:
            new_node_link=False

        if new_node_link:
            networkfiles.add_node_link(n, new_node_link)

        #If the var is true, remove the node and do not do any of the below
        if delete_node_name:
            networkfiles.remove_node(n)
        #If this is true, then that means the node name changed, so use the new node name
        elif (new_node_name != n):

           networkfiles.change_node_name(n, new_node_name)
           if (new_node_hostname != current_node_hostname):
                networkfiles.change_node_hostname(new_node_name, new_node_hostname)
           if (int(new_node_replicas) != int(current_node_replicas)):
                networkfiles.change_node_replicas(new_node_name, int(new_node_replicas))
           if (int(new_node_priority) != int(current_node_priority)):
                networkfiles.change_node_priority(new_node_name, int(new_node_priority))
        else:
           if (new_node_hostname != current_node_hostname):
                networkfiles.change_node_hostname(n, new_node_hostname)
           if (int(new_node_replicas) != int(current_node_replicas)):
                networkfiles.change_node_replicas(n, int(new_node_replicas))
           if (int(new_node_priority) != int(current_node_priority)):
                networkfiles.change_node_priority(n, int(new_node_priority))

    networkfiles.graph()
    graphiframe()
    networkfiles.load_nodes_to_edit()
    return graph()