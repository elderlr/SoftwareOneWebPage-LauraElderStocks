#created by Laura Elder using the following resources:
#[1] https://docs.microsoft.com/en-us/visualstudio/ide/quickstart-python?view=vs-2019
#[2] https://codeforgeek.com/render-html-file-in-flask/
#[3] https://flask.palletsprojects.com/en/2.0.x/quickstart/#a-minimal-application
#[4] https://www.askpython.com/python-modules/flask/flask-redirect-url
#[5] https://www.geeksforgeeks.org/read-json-file-using-python/

import yfinance as yf
import time
import os
import numpy as np
import sys, select, os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import json
#import pullSaidImage
import display_info
from flask import Flask
from flask import url_for
from flask import render_template
from flask import redirect, request, abort

# Create an instance of the Flask class that is the WSGI application.
# The first argument is the name of the application module or package,
# typically __name__ when using a single module.
app = Flask(__name__)

# Flask route decorators map / and /hello to the hello function.
# To add other resources, create functions that generate the page contents
# and add decorators to define the appropriate resource locators for them.

@app.route('/')
@app.route('/home')
def home():
    # Render the page
    return render_template('form.html')

@app.route('/assets')
def assetsPage():
    # Render the page
    return render_template('assets.html')

@app.route('/patterns')
def patternsPage():
    # Render the page
    return render_template('patterns.html')

@app.route('/Hammer')
def pattern_returnPage():
    pattern_pass = "Hammer"
    signal = "Buy"
    image = "someone"
    #call Elain's service
    user_query = 'candlestick pattern'
    location = 'C:\\Users\\Laura\\source\\repos\\SoftwareOneWebPage-LauraElderStocks\\search_results.json'
    infor=display_info.display_info(user_query, location)
    #go get the data from service
    # Opening JSON file
    f = open(location,)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    # Iterating through the json
    max = data['results']
    oi = dict([(ma['summary'], ma) for ma in max])
    going =""
    for j in oi:
        if going == "":
            going = going + j
    information = going
    # Closing file
    f.close()
    return render_template('pn.html', patternZ = pattern_pass, signal=signal, image=image, information=information)

@app.route('/entry', methods = ['POST', 'GET'])
def entry():
    if request.method == 'POST':
        name = request.form['name']
        return redirect(f"/search/{name}")

@app.route('/search/<name>')
def searchPage(name):
   symbol = request.args.get(name, default="BTC-USD")
   period = request.args.get('period', default="1mo")
   interval = request.args.get('interval', default="1d")        
   quote = yf.Ticker(symbol)   
   hist = quote.history(period=period, interval=interval)
   data = hist.to_json()
   filename ='C:\\Users\\Laura\\source\\repos\\SoftwareOneWebPage-LauraElderStocks\\stocks.json'
   with open(filename,'w') as file_object:
    json.dump(data,file_object)
    price = '100.00'
    action = "Buy"
    pattern="Hammer"
   return render_template('analysis.html', name =name, price = price, action= action, pattern=pattern)
   #return data
   #return quote.info

@app.route("/quote")
def display_quote():
  symbol = request.args.get('symbol', default="AAPL")
  quote = yf.Ticker(symbol)
  return quote.info

if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.run('localhost', 4449)
