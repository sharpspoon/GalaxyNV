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
        links=networkfiles.link_list()
    )

@app.route('/image')
def image():
    return render_template(
        'image.html',
        title='Galaxy Image and Network Configuration',
        year=datetime.now().year
    )

@app.route('/contact')
def contact():
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/networkyaml')
def networkyaml():
    ymlcontent = networkfiles.loadfiles()
    jsoncontent = networkfiles.loadjsonfiles()

    return render_template(
        'networkyaml.html',
        yc = ymlcontent,
        jc = jsoncontent
    )

#Pyvis graph html page
@app.route('/graph')
def graph():
    loadnodes=networkfiles.load_nodes_to_edit()
    javascript=networkfiles.build_add_link_page_scripts()
    return render_template(
        'graph.html',
        nodes=loadnodes,
        js=javascript
    )

#Force directed graph with no bridge display
@app.route('/fdg')
def fdg():
    jsoncontent = networkfiles.create_d3json()
    return render_template(
        'fdg.html',
        jc = jsoncontent
    )

#Force directed graph with a bridge display
@app.route('/fdgbridge')
def fdgbridge():
    jsoncontent = networkfiles.create_d3jsonbridge()
    return render_template(
        'fdgbridge.html',
        jc = jsoncontent
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
    networkfiles.graph()
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
@app.route('/addnode', methods =["GET", "POST"])
def addnode():
    node_name = request.form.get("nodeName")
    node_link = request.form.get("nodeLink")
    image_name = request.form.get("imageName")
    number_of_nodes = request.form.get("numberOfNodes")
    networkfiles.add_node(node_name, node_link, image_name, number_of_nodes)
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
        delete_node_name = request.form.get("delete_"+n)
        try:
            current_node_replicas=data1["nodes"][n]["replicas"]
        except:
            current_node_replicas=0
        new_node_replicas = request.form.get("replicas_"+n)
        for l in data1["nodes"][n]["links"]:
            delete_link_name = request.form.get("delete_"+n+"_"+l)
            if delete_link_name:
                if globals.DEBUG==True:
                    print ('Deleting the link: '+n+' ---> '+l)
                networkfiles.remove_node_link(n, l)

        #If the var is true, remove the node and do not do any of the below
        if delete_node_name:
            if globals.DEBUG==True:
                print ('Deleting the node "'+n+'" and ignoring any other changes to this node. Moving on to next node...')
            networkfiles.remove_node(n)

        #Check if the name of the node has changed
        elif (new_node_name != n) and (int(new_node_replicas) != int(current_node_replicas)):
            networkfiles.change_node_name(n, new_node_name)
            if globals.DEBUG==True:
                print ('new_node_name='+str(new_node_name))
                print ('n='+str(n))
                print ('new_node_replicas='+str(new_node_replicas))
                print ('current_node_replicas='+str(current_node_replicas))
            networkfiles.change_node_replicas(new_node_name,current_node_replicas, new_node_replicas)

        elif new_node_name != n:
            if globals.DEBUG==True:
                print ('new_node_name='+str(new_node_name))
                print ('n='+str(n))
            networkfiles.change_node_name(n, new_node_name)

        #Check if the replicas of the node has changed
        elif int(new_node_replicas) != int(current_node_replicas):
            if globals.DEBUG==True:
                print ('new_node_replicas='+str(new_node_replicas))
                print ('current_node_replicas='+str(current_node_replicas))
            networkfiles.change_node_replicas(n,current_node_replicas, int(new_node_replicas))

    graphiframe()
    networkfiles.load_nodes_to_edit()
    return graph()