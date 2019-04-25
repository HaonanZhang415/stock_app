# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 16:57:38 2019

@author: Zhang
"""

# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# [START gae_python37_app]
from flask import Flask, render_template, redirect, url_for, request
from iexfinance.stocks import Stock
import datetime
import pytz
from pytz import timezone

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def home():
    """Return a friendly HTTP greeting."""
    return 'FINALLY!!!!!!!!!!'

@app.route('/welcome')
def hello2():

    return render_template('welcome.html')

@app.route('/stock', methods = ['GET', 'POST'])
def stock():
    error = None
    output1 = None
    output2 = None
    output3 = None
    if request.method == "POST":
        
    
        currentDT = datetime.datetime.now()
        
        company = request.form["Symbol"]
        stock_object = Stock(company)
        
        print(company)
        
        try:
            stock_object.get_company_name()   
        except:
            error = 'Invalid Symbol. Please try again.'
            return render_template('stock.html', error=error)

        print (currentDT.strftime("%a %b %d %H:%M:%S PDT %Y"))
        print (stock_object.get_company_name(), '(' + company + ')')
        
        #previous_day_price = stock_object.get_previous_day_prices()['close']
        #print(previous_day_price)
        print(stock_object.get_quote())
        try:
            curr_price = round(stock_object.get_quote()['iexRealtimePrice'], 2)
        except:
            curr_price = round(stock_object.get_quote()['close'], 2)
        #pre_close = stock_object.get_quote()['close']
        change = round(stock_object.get_quote()['change'], 2)
        
        
        percentage = symbolFunc(round(stock_object.get_quote()['changePercent'] * 100, 2))
        change = symbolFunc(change)
        
        print (curr_price, change, '(' + str(percentage) + '%)') 
        
        date_format = "%a %b %d %H:%M:%S PDT %Y"
        company = company.upper()
        #output1 = currentDT.strftime(date_format)
        
        date_fixed = currentDT.astimezone(timezone('US/Pacific'))
        date_fixed = date_fixed.strftime(date_format)
        
        output2 = stock_object.get_company_name() + '    (' + company + ')'
        output3 = str(curr_price) + '    ' + change + '    (' + str(percentage) + '%)'
        
        return render_template('stock.html', error=error, output1 = date_fixed, output2 = output2, output3 = output3)
    
    return render_template('stock.html', error=error)

def checkSymbol(company):
    
    stock_object = Stock(company)
    
    try:
        stock_object.get_company_name()
    except:
        print ("Invalid symbol! Please input again:")
        return checkSymbol()
            
    return stock_object, company

def symbolFunc(value):
    if value < 0:
        return str(value)
    else:
        return '+' + str(value)
    
# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run()#host='127.0.0.1', port=8000, debug=True
# [END gae_python37_app]