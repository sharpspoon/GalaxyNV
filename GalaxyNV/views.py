from datetime import datetime
from flask import Flask, request, render_template, send_file
from GalaxyNV import app, gnx, networkfiles
import yaml

@app.route('/')
@app.route('/home')
def home():
    subheader1 = gnx.subheader1()
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        sh1=subheader1
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

@app.route('/about')
def about():
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

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

@app.route('/demoiframe')
def demoiframe():
    return render_template(
        'Demo.html'
    )

@app.route('/demojson')
def demojson():
    return render_template(
        'NetworkFiles/json/demo.json'
    )

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

#Pyvis graph
@app.route('/graph')
def graph():
    return render_template(
        'graph.html'
    )

@app.route('/graphiframe')
def graphiframe():
    networkfiles.graph()
    return render_template(
        'PyvisGraph.html'
    )

#Force directed graph with no bridge display
@app.route('/fdg')
def fdg():
    jsoncontent = networkfiles.create_d3json()
    return render_template(
        'fdg.html',
        jc = jsoncontent
    )

@app.route('/fdgiframe')
def fdgiframe():
    return render_template(
        'ForceDirectedGraph.html'
    )

#Force directed graph with a bridge display
@app.route('/fdgbridge')
def fdgbridge():
    jsoncontent = networkfiles.create_d3jsonbridge()
    return render_template(
        'fdgbridge.html',
        jc = jsoncontent
    )

@app.route('/fdgbridgeiframe')
def fdgbridgeiframe():
    return render_template(
        'ForceDirectedGraphBridge.html'
    )

@app.route('/arc')
def arc():
    jsoncontent = networkfiles.create_d3json()
    return render_template(
        'arc.html',
        jc = jsoncontent
    )

@app.route('/arciframe')
def arciframe():
    return render_template(
        'ArcGraph.html'
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

@app.route('/addnode', methods =["GET", "POST"])
def addnode():
    node_name = request.form.get("nodeName")
    node_link = request.form.get("nodeLink")
    image_name = request.form.get("imageName")
    number_of_nodes = request.form.get("numberOfNodes")
    networkfiles.add_node(node_name, node_link, image_name, number_of_nodes)
    graphiframe()
    return render_template(
        'graph.html'
        )

@app.route('/removenode', methods =["GET", "POST"])
def removenode():
    node_name = request.form.get("nodeName")
    networkfiles.remove_node(node_name)
    graphiframe()
    return render_template(
        'graph.html'
        )