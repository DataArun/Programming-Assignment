#Folder operations

import os
# API flask app
from flask import Flask, request
from flask.ext.jsonpify import jsonify
from flask import Response
from flask.ext.cache import Cache
# Panadas for dataframes
import pandas as pd
# Ouput Json format to the user
import json    
# Work with date in the data
import datetime
from datetime import date, timedelta
# Enabling Caching ability
import requests_cache
# For Multiprocessing
from multiprocessing import Pool


requests_cache.install_cache('demo_cache')
app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
_pool = None
app.cache = Cache(app)  

folder = os.getcwd()+"\\Data\\"
#folder = "C:\\Users\\Arun Kumar\\Documents\\train\\"
currecnylist = ["CHF","EUR","GBP","OMR","BHD","KWD","SGD"]
# function for task 1 Given a date it will retrieve the currency rate of all currecny
def task1(dateRangeA):
        dateRangeA= dateRangeA.strip()
        resp = ""
        outputList = []
        try:
            datetime.datetime.strptime(dateRangeA, '%Y-%m-%d')
        except:
            resp = Response(json.dumps({"Message":"Incorrect data format, should be YYYY-MM-DD"}), status=404, mimetype='application/json')
        if(resp==""):
            try:
                dateRangeA= dateRangeA
                jsonOutput = {}
                datafile = pd.read_csv(folder  + dateRangeA+ ".txt", sep="\t")
                olyDate = datafile[['Currency','Amount']]
                for Index,i in olyDate.iterrows():
                     outputJson = {
                             "Currency":i["Currency"],
                             "Conversion Rate" :i["Amount"]
                             }
                     outputList.append(outputJson)
                     jsonOutput  = json.dumps(outputList)
                resp = Response(jsonOutput, status=200, mimetype='application/json')
            except :
                resp = Response(json.dumps({"Message":"Data not found for the date"}), status=200, mimetype='application/json')
        return resp

# function for task 2 Given a date  and two currency, it will retrieve the conversion between the two currency.
def task2(dateRangeA,currencyA,currencyB):
        resp = ""
        try:
            dateRangeA= dateRangeA
            currencyA = currencyA
            currencyB =  currencyB
            dateRangeA= dateRangeA.strip()
            currencyA = currencyA.strip().upper()
            currencyB =  currencyB.strip().upper()
            
            try:
                datetime.datetime.strptime(dateRangeA, '%Y-%m-%d')
            except:
                resp = Response(json.dumps({"Message":"Incorrect data format, should be YYYY-MM-DD"}), status=404, mimetype='application/json')
            if (currencyA not in currecnylist):
                resp = Response(json.dumps({"Message":"From Currency is not present in the list. Kindly verify the input"}), status=404, mimetype='application/json')
            elif(currencyB not in currecnylist):
                resp = Response(json.dumps({"Message": "To Currency is not present in the list. Kindly verify the input"}), status=404, mimetype='application/json')
                
            if(resp==""):  
                try:
                    datafile = pd.read_csv(folder  + dateRangeA+ ".txt", sep="\t")
                    outputList = []
                    currencyAValue =datafile[(datafile.Currency == currencyA)]["Amount"]
                    currencyAValue = currencyAValue.iloc[0]
                    currencyBValue =datafile[(datafile.Currency== currencyB)]["Amount"]
                    currencyBValue = currencyBValue.iloc[0]
                    convrsionRate = float(currencyAValue /currencyBValue) 
                    outputJson = {
                                "From Currency": currencyA ,
                                "To Currency": currencyB,
                                "Conversion Rate" : convrsionRate,
                                "Date" : dateRangeA
                                }
                    outputList.append(outputJson)
                    jsonOutput  = json.dumps(outputList)
                    resp = Response(jsonOutput, status=200, mimetype='application/json')
                except:
                    
                    resp = Response(json.dumps({"Message":"Data not found for the date"}), status=404, mimetype='application/json')
        except:
                resp = Response(json.dumps({"Message":"Unexpected error"}), status=404, mimetype='application/json')
        return resp
        

# function for task 3 Given a date  range and a currency, it will retrieve the currency for the entire range.
def task3(dateRangeA,dateRangeB,currencyA):
        resp= ""     
        dateRangeA= dateRangeA.strip()
        dateRangeB= dateRangeB.strip()
        currencyA = currencyA.strip().upper()
        try:
            datetime.datetime.strptime(dateRangeA, '%Y-%m-%d')
        except:
            resp = Response(json.dumps({"Message":"Incorrect From data format, should be YYYY-MM-DD"}), status=404, mimetype='application/json')
        try:
            datetime.datetime.strptime(dateRangeB, '%Y-%m-%d')
        except:
            resp = Response(json.dumps({"Message":"Incorrect To data format, should be YYYY-MM-DD"}), status=404, mimetype='application/json')
        if (currencyA not in currecnylist):
            resp = Response(json.dumps({"Message":"From Currency is not present in the list. Kindly verify the input"}), status=404, mimetype='application/json')

        if(resp==""):     
            yyyy1,mm1,dd1 = dateRangeA.split("-")
            yyyy2,mm2,dd2 = dateRangeB.split("-")
            

            d1 = date(int(yyyy1), int(mm1), int(dd1))
            d2 = date(int(yyyy2), int(mm2), int(dd2))
            delta = d2 - d1
            
            #Enabling multiprocessing
            p = Pool(processes = 4)    
            actDate = []
            for i in range(delta.days + 1):
                actDate.append(str(d1 + timedelta(days=i)))    
            data = [x for x in  p.map(multirange ,([(i,currencyA) for i in actDate ])) if x is not None]
            p.close()
            jsonOutput1  = json.dumps(data)
            resp = Response(jsonOutput1, status=200, mimetype='application/json')
        return resp

# Task 3 's subordinate function to process the data.   
def multirange(*args):
    actDate1 = args[0][0]
    currencyA = args[0][1]
    jsonOutput = None
    outputJson= None
    try:
                outputList = []
                datafile = pd.read_csv(folder  + actDate1 + ".txt", sep="\t")
                currencyAValue =datafile[(datafile.Currency == currencyA)]["Amount"]
                currencyAValue = currencyAValue.iloc[0]
                outputJson = {
                        "Date": actDate1 ,
                        "Currency" : currencyA,
                        "Conversion Rate" : currencyA,
                        }
                jsonOutput  = json.dumps(outputList)
    except:
        1+1
    if(jsonOutput == [] or jsonOutput == None or jsonOutput == "" ):
        1+1
    else:
        return outputJson
    
#Error handling for api if page not found
@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp



@app.route('/Date/<dateRangeA>')
@app.cache.memoize(timeout=300)

# Task 1 API call with caching enabled
def api_root1(dateRangeA):
        r = task1(dateRangeA)
        return r
    
@app.route('/CurrencyRange/<dateRangeA>/<currencyA>/<currencyB>')
@app.cache.memoize(timeout=300)
# Task 2 API call with caching enabled
def api_root2(dateRangeA,currencyA,currencyB):
        r = task2(dateRangeA,currencyA,currencyB)        
        return r
    
# Task 3 API call with caching enabled
@app.route('/Daterange/<dateRangeA>/<dateRangeB>/<currencyA>')
@app.cache.memoize(timeout=300)
def api_root3(dateRangeA,dateRangeB,currencyA):
        r = task3(dateRangeA,dateRangeB,currencyA)
        return r


# Main function which creates the sequence of execution
if __name__ == '__main__':

    try:
    # App runs in the path : http://127.0.0.1:5002/
        app.run(port=5002)
    #Stop the process of API
    except KeyboardInterrupt:
        _pool.close()
        _pool.join()
