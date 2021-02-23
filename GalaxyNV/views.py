"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from GalaxyNV import app, gnx



@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    subheader1 = gnx.subheader1()
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        sh1=subheader1
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/json')
def json():
    """Renders the about page."""
    return render_template(
        'miserables.json'
    )

@app.route('/fdgiframe')
def fdgiframe():
    """Renders the about page."""
    return render_template(
        'ForceDirectedGraph.html'
    )

@app.route('/demoiframe')
def demoiframe():
    """Renders the about page."""
    return render_template(
        'Demo.html'
    )

@app.route('/demojson')
def demojson():
    """Renders the about page."""
    return render_template(
        'demo.json'
    )

@app.route('/fdg')
def fdg():
    """Renders the about page."""
    return render_template(
        'fdg.html'
    )
