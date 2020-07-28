from flask import Flask,json,jsonify
from flask_cors import CORS, cross_origin
import pathlib

## order declare params
orderData= 'orders'
ordersDataPath = orderData+ "/orders.json"  ## Set file name to open

### read file
file = pathlib.Path(ordersDataPath)
if file.exists ():                          ##  TEST CASE:  file exists
    with open(ordersDataPath) as data:
        getOrderJSON = json.load(data)
else:                                       ##  TEST CASE:  file NOT exists
    getOrderJSON=json.load('{}')            ## return empty json for UI to display "loading"


## 2. INITIALIZE API
api = Flask(__name__)
## CORS(app)
cors = CORS(api, resources={r"/foo": {"origins": "*"}})
api.config['CORS_HEADERS'] = 'Content-Type'


## 3. INITIALIZE API ROUTE TO CALL IN BROWSER
@api.route('/api/orders/', methods=['GET','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])

## 3a. DEFINE FUNCTION for route to get  data json formatted
def get_getorderdata():
  return jsonify(getOrderJSON)

### save for later db version
# def list_orders():
#     orders = firestore.list_collection(u'Order')
#     return render_template("order_list.html", orders=orders)



## 4. INITIALIZE API ROUTE TO CALL IN BROWSER
@api.route('/api/orders/:id', methods=['GET','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])

## 4a. DEFINE FUNCTION for route to get  data json formatted
def get_getathletedata():
  return jsonify(getAtheleteJSON)

if __name__ == '__main__':
    api.run()


