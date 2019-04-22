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
from flask import Flask
from iexfinance.stocks import Stock
import datetime

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

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
@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/company/<inputy>')
def hello(inputy):
    """Return a friendly HTTP greeting."""
    #return 'Hello World!'

    print('Program Started!')
    currentDT = datetime.datetime.now()
    
    stock_object, company = checkSymbol(inputy)
    
    print (currentDT.strftime("%a %b %d %H:%M:%S PDT %Y"))
    print (stock_object.get_company_name(), '(' + company + ')')
    
    all_price = stock_object.get_previous_day_prices()
    
    
    curr_price = stock_object.get_previous_day_prices()['close']
    open_price = stock_object.get_previous_day_prices()['open']
    change = stock_object.get_previous_day_prices()['change']
    
    
    percentage = symbolFunc(round(change/open_price * 100, 2))
    change = symbolFunc(change)
    print (curr_price, change, '(' + str(percentage) + '%)') 





if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]