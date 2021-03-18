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

@app.route('/json')
def json():
    return render_template(
        'fdg.json'
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
