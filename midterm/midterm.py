from flask import Flask, request, render_template, redirect, url_for, flash, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required

import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

class NameForm(FlaskForm):
    itunes = StringField('What is your favorite movie?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/')
def home():
    respo = make_response("Hello there, movie world.")
    respo.set_cookie("myname", "Jamie")
    return respo

@app.route('/itunes', methods= ['GET','POST'])
def index():
    simpleForm = NameForm()
    return render_template('itunes.html', form=simpleForm)

@app.route('/season', methods = ['POST'])
def result():
    form = NameForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        itunes = form.itunes.data
        base_url= 'https://itunes.apple.com/search?term='
        url= base_url+ itunes
        x= requests.get(url, params= {"entity": "movie"}).text
       	data = json.loads(x)
       	return render_template('season.html', apiresult= data)


@app.route('/movie/<movie>', methods = ['GET', 'POST'])
def result1(movie):
    base_url= 'https://itunes.apple.com/search?term='
    url= base_url + movie
    x= requests.get(url, params= {"entity": "movie"}).text
    data = json.loads(x)
    return render_template('specificmovie.html', apiresult= data)

@app.errorhandler(404)
def file404(a):
    return render_template('404.html'), 404


@app.errorhandler(405)
def file405(a):
    return render_template('405.html'), 405

## in order to get 405 error go to localhost5000/season in browser

##in order to see jinja conditional statement search Shrek on homepage

        

        
if __name__ == '__main__':
    app.run()





