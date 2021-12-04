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

@app.route('/entry', methods = ['POST', 'GET'])
def entry():
    if request.method == 'POST':
        name = request.form['name']
        return redirect(f"/search/{name}")

@app.route('/search/<name>')
def searchPage(name):
    filename ='C:\\Users\\Laura\\source\\repos\\SoftwareOneWebPage-LauraElderStocks\\stocks.json'
    #with open(filename,'w') as file_object:
     #   json.dump(data,file_object)
    temp = {"yf":[]}
    with open(filename, "w") as outfile:
        json.dump(temp, outfile)
    outfile.close()
    #get the item we are searching for
    symbol = request.args.get(name, default="BTC-USD")
    period = request.args.get('period', default="1wk")
    interval = request.args.get('interval', default="1d") 
    quote = yf.Ticker(symbol)   
    hist = quote.history(period=period, interval=interval)
    hist = hist.reset_index()
#build the various arrays
    d = []
    o = []
    h = []
    l = []
    c = [] 
    count = 0
    day = 0
    month = 0
    year = 0
    date_var = ""
    for j in hist['Date']:
        #count the number of dates
        count = count + 1
        day = j.day
        month = j.month
        year = j.year
        date_var = str(month)+"/"+str(day)+"/"+str(year)
        d.append(date_var)
    for j in hist['Open']:
        o.append(j)
    for j in hist['High']:
        h.append(j)
    for j in hist['Low']:
        l.append(j)
    for j in hist['Close']:
        c.append(j)
    # insert data into the Json filename
    for i in range(count):
        Date = d[i]
        Open = o[i]
        High = h[i]
        Low = l[i]
        Close = c[i]
        data = {'Date':Date,'Open':Open,'High':High,'Low':Low,'Close':Close}
        with open(filename,'r+') as file:
              # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data["yf"].append(data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
    #go through the json file and get out the price
    with open(filename,"r") as file:
        working = json.load(file)
        j = count - 1
        for j in working["yf"]:
            today_data = j['Close']
    price = today_data
    # get the last three days of data

    #calculate the pattern and establish the action
    action = "Buy"#change this Laura
    pattern="Hammer"#change this Laura
    #call elains service to find information on the asset
    user_query = name
    location = 'C:\\Users\\Laura\\source\\repos\\SoftwareOneWebPage-LauraElderStocks\\search_results.json'
    infor=display_info.display_info(user_query, location)
    #go get the data from service
    # Opening JSON file
    f = open(location,)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    # Iterating through the json
    information = data['summary'] 
    # Closing file
    f.close()
    return render_template('analysis.html', name =name, price = price, action= action, pattern=pattern, information=information)
    #return data
    #return quote.info

@app.route("/quote")
def display_quote():
  symbol = request.args.get('symbol', default="AAPL")
  quote = yf.Ticker(symbol)
  return quote.info

@app.route('/Hammer')
def pattern_returnPage():
    pattern_pass = "Hammer"
    signal = "Buy"
    #call Elain's service
    user_query = 'Hammer_(candlestick_pattern)'
    location = 'C:\\Users\\Laura\\source\\repos\\SoftwareOneWebPage-LauraElderStocks\\search_results.json'
    infor=display_info.display_info(user_query, location)
    #go get the data from service
    # Opening JSON file
    f = open(location,)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    # Iterating through the json
    information = data['summary'] 
    # Closing file
    f.close()
    return render_template('pn.html', patternZ = pattern_pass, signal=signal, information=information)

@app.route('/Inverse')
def pattern_returnPageI():
    pattern_pass = "Inverse Hammer/ Inverted Hammer"
    signal = "Buy"
    #call Elain's service
    user_query = 'Inverted_hammer'
    location = 'C:\\Users\\Laura\\source\\repos\\SoftwareOneWebPage-LauraElderStocks\\search_results.json'
    infor=display_info.display_info(user_query, location)
    #go get the data from service
    # Opening JSON file
    f = open(location,)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    # Iterating through the json
    information = data['summary'] 
    # Closing file
    f.close()
    return render_template('pn.html', patternZ = pattern_pass, signal=signal, information=information)

@app.route('/Morning')
def pattern_returnPageM():
    pattern_pass = "Morning Star"
    signal = "Buy"
    #call Elain's service
    user_query = 'Morning_star_(candlestick_pattern)'
    location = 'C:\\Users\\Laura\\source\\repos\\SoftwareOneWebPage-LauraElderStocks\\search_results.json'
    infor=display_info.display_info(user_query, location)
    #go get the data from service
    # Opening JSON file
    f = open(location,)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    # Iterating through the json
    information = data['summary'] 
    # Closing file
    f.close()
    return render_template('pn.html', patternZ = pattern_pass, signal=signal, information=information)

@app.route('/White')
def pattern_returnPageW():
    pattern_pass = "Three White Soldiers"
    signal = "Buy"
    #call Elain's service
    user_query = 'Three_white_soldiers'
    location = 'C:\\Users\\Laura\\source\\repos\\SoftwareOneWebPage-LauraElderStocks\\search_results.json'
    infor=display_info.display_info(user_query, location)
    #go get the data from service
    # Opening JSON file
    f = open(location,)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    # Iterating through the json
    information = data['summary'] 
    # Closing file
    f.close()
    return render_template('pn.html', patternZ = pattern_pass, signal=signal, information=information)

@app.route('/Hanging')
def pattern_returnPageH():
    pattern_pass = "Hanging Man"
    signal = "Sell"
    #call Elain's service
    user_query = 'Hanging_man_(candlestick_pattern)'
    location = 'C:\\Users\\Laura\\source\\repos\\SoftwareOneWebPage-LauraElderStocks\\search_results.json'
    infor=display_info.display_info(user_query, location)
    #go get the data from service
    # Opening JSON file
    f = open(location,)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    # Iterating through the json
    information = data['summary'] 
    # Closing file
    f.close()
    return render_template('pn.html', patternZ = pattern_pass, signal=signal, information=information)

@app.route('/Crow')
def pattern_returnPageCRO():
    pattern_pass = "Three Black Crows"
    signal = "Sell"
    #call Elain's service
    user_query = 'Three_black_crows'
    location = 'C:\\Users\\Laura\\source\\repos\\SoftwareOneWebPage-LauraElderStocks\\search_results.json'
    infor=display_info.display_info(user_query, location)
    #go get the data from service
    # Opening JSON file
    f = open(location,)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    # Iterating through the json
    information = data['summary'] 
    # Closing file
    f.close()
    return render_template('pn.html', patternZ = pattern_pass, signal=signal, information=information)


if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.run('localhost', 4449)
