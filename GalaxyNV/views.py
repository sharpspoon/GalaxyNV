from datetime import datetime
from flask import render_template
from GalaxyNV import app, gnx, networkfiles



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

@app.route('/json')
def json():
    return render_template(
        'network.json'
    )

@app.route('/fdgiframe')
def fdgiframe():
    return render_template(
        'ForceDirectedGraph.html'
    )

@app.route('/demoiframe')
def demoiframe():
    return render_template(
        'Demo.html'
    )

@app.route('/demojson')
def demojson():
    return render_template(
        'demo.json'
    )

@app.route('/fdg')
def fdg():
    return render_template(
        'fdg.html'
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
