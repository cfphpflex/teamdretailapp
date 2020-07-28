from flask import Flask,json,jsonify
from flask_cors import CORS, cross_origin
import pathlib

##  https://stoplight.io/blog/python-rest-api/
## TEST DATA PLACEHOLDER  companies = [{"id": 1, "name": "BBall Player One"}, {"id": 2, "name": "BBall Player Two"}]

## 1. Open the file; LATER REPLACE WITH SQL DATA CALL TO DATABASE TO GET DATA AND FORMAT AS JSON RESPONSE TEST JSON   https://jsonformatter.curiousconcept.com/
## for team, indiv athtlete, depends on who is loggedin (admin, or indiv athlete)

orderData= 'orders';
###athleteFirstLastname = "ADAMS_CARLEY"    ## SET NAME VALUE FROM LOGGEDIN SESSION USER PROFILE OR SELECTED NAME BY ADMIN USER ROLE

## if value is all: get all data json file, else value is indiv athlete, get one athlete data file
##   https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_select select example

ordersDataPath = orderData+ "/orders.json"  ## Set file name to open

file = pathlib.Path(ordersDataPath)
if file.exists ():                          ##  TEST CASE:  file exists
    with open(ordersDataPath) as data:
        getOrderJSON = json.load(data)
else:                                       ##  TEST CASE:  file NOT exists
    getOrderJSON=json.loads('{}')            ## return empty json for UI to display "loading"


## 2. INITIALIZE API
api = Flask(__name__)
## CORS(app)
cors = CORS(api, resources={r"/foo": {"origins": "*"}})
api.config['CORS_HEADERS'] = 'Content-Type'


## 3. INITIALIZE API ROUTE TO CALL IN BROWSER
@api.route('/api/orders/', methods=['GET','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])

## 4. DEFINE FUNCTION for route to get  data json formatted
def get_getathletedata():
  return jsonify(getAtheleteJSON)

if __name__ == '__main__':
    api.run()


## 4. INITIALIZE API ROUTE TO CALL IN BROWSER
@api.route('/api/orders/:id', methods=['GET','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])

## 4. DEFINE FUNCTION for route to get  data json formatted
def get_getathletedata():
  return jsonify(getAtheleteJSON)

if __name__ == '__main__':
    api.run()


