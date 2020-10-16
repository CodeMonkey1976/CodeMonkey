import json
from bson.json_util import dumps
import datetime
import bottle
from bottle import post, route, run, request, abort
import pymongo
import yaml

connection = pymongo.MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']

#Retrieve Details & read in business record using same Code...Retrieve
#Method retrieves Information based on Stock Ticker
def retrieve_Stock_Query(ticker):
  query = {"Ticker": str(ticker)}
  try:
    result = dumps(collection.find(query))
    if result[0] == "[":
      result = result[1:]
      result = result[:-1]
    return json.loads(result)
  except:
    return 0

# set up URI paths for REST service

# Reteive Details
@route('/retreiveDetails', method = 'GET')

def retreiveDetails():  
  ticker = request.query.ticker
  details = request.query.details
  ticker = ticker.encode("utf-8")
  details = details.encode("utf-8")
  result = retrieve_Stock_Query(ticker)
  if result:
    return str(result[details])
  else:
    return "Not Found"

  

  
  
#Sector Search
@route('/sectorSearch', method = 'GET')
def industrySearch():
  industry = request.query.industry
  
  industry = industry.replace('$AND$', '&')  
  industry = industry.replace('%20', " ")  
  
  result = collection.aggregate(
    [
    {"$match": {"Sector": industry}},
      {"$group": {"_id": "$Sector", "Shares Outstanding": {"$sum": "$Shares Outstanding"}}}           
    ])
  my_list =[]
  for i in result:
    my_list.append("Outstanding Shares = " + str(i["Shares Outstanding"]))
  return my_list
    

#Industry search
@route('/industrySearch', method = 'GET')
def industrySearch():
  industry = request.query.industry
  industry = industry.replace('$AND$', '&')  
  industry = industry.replace('%20', " ")  
  query = {'Industry': str(industry)}
  #print(query)
  result = collection.find(query)  
  tickers = []
  
  for index in result:
    payload = "Company = " + str(index['Company']) + "Ticker = " + str(index['Ticker'])    
    tickers.append(payload)

  for i in tickers:
    print i
   
  return tickers

# High Low
@route('/stock_range', method='GET')
def stock_range():
  low = request.query.low
  high = request.query.high
  query = {"Price" : {"$gte" : int(str(low)), "$lte" : int(str(high))}}
  
  print(query)
  result = json.loads(dumps(collection.find(query).sort("Return on Investment", pymongo.DESCENDING).limit(10)))
  company_list = []
  for i in range(len(result)):
    record = json.dumps(result[i])  # dumps changes data from unicode to dictionary
    record = yaml.safe_load(record)    
    company_list.append(record["Ticker"])
    
  company_string_list = "" 
  for i in company_list:
    company_string_list = company_string_list + i + " '''"

  company_string_list = company_string_list[:-3]
  return company_string_list




# High Low
@route('/highLow', method='GET')
def highLow():
  low = request.query.low
  high = request.query.high
  query = {"50-Day Simple Moving Average" : {"$gte" : int(str(low)), "$lte" : int(str(high))}}
  
  result = collection.find(query).count()  
  return json.loads(json.dumps(str(result), indent=4, default=json_util.default))


@route('/deleteStock', method='GET')
def delete():
    ticker = request.query.stock_ticker
    data = {'Ticker': ticker}
    exist = collection.find(data).count()
    my_message = "Record Not Found"
    if exist:
        collection.remove(data)
        my_message = "Record Deleted"
    return my_message

  
# Update Entry
@route('/updateEntry', method='GET')
def update():
  try:
      
      stock_ticker = request.query.stock_ticker
      stock_price = request.query.stock_price
      data = {'Ticker': stock_ticker}      
      payload = {"Ticker": stock_ticker, "Price": stock_price}
      data = {"Ticker": stock_ticker}
      exist = collection.find(data).count()
      
      if not exist:
        message = "Record Does Not Exist"
      
      else:
        id = collection.find_one(data).get("_id")
        newInfo = {"$set": {"Price": stock_price}}
        collection.update_one(data, newInfo)
        message = "Record Updated"
        
  except:
      message = "Error Connecting to Server"
      
  return message

  
# Create Entry
@route('/createEntry', method = 'GET')
def createEntry():
    try:
      # data = {'Ticker': stock_ticker}
      stock_ticker = request.query.stock_ticker
      stock_price = request.query.stock_price
      data = {'Ticker': stock_ticker}
      
      payload = {"Ticker": stock_ticker, "Price": stock_price}
      data = {"Ticker": stock_ticker}
      exist = collection.find(data).count()
      if not exist:
        collection.insert_one(payload)
        message = "Record Created"
      
      else:
        message = "Record Already Exists"
        
    except:
      message = "Error Connecting to Server"
      
    return message

#read in business record
@route('/getStock', method='GET')
def readMe():
    result = "Not Found"
    try:
        request.query.stock_ticker
        ticker = request.query.stock_ticker       
        result = retrieve_Stock_Query(ticker)        
        return result
   
    except:
      return the_Record

#greatings
@route('/hello', method='GET')
def get_greeting():
    try:
        request.query.name
        name = request.query.name
        if name:
            string = "{\"Hello, \"" + request.query.name + "\"}"
    except NameError:
        abort(404, 'No parameter for id %s' % id)
    if not string:
        abort(404, 'No id %s' % id)
    return json.loads(json.dumps(string, indent=4, default=json_util.default))


#strings for hello world
@post('/strings')
def post_strings():
    print(busniess_List)
    data = request.body.readline()
    entity = json.loads(data)
    string1 = entity["string1"]
    string2 = entity["string2"]
    return {'First': string1, 'Second': string2}

# Display current time....
@route('/currentTime', method='GET')
def get_currentTime():
    dateString = datetime.datetime.now().strftime("%Y-%m-%d")
    timeString = datetime.datetime.now().strftime("%H:%M:%S")
    string = "{\"date\":" + dateString + ",\"time\":" + timeString + "}"
    return json.loads(json.dumps(string, indent=4, default=json_util.default))

# create new record
@post('/create')
def addOne():
    data = request.body.readline()
    entity = json.loads(data)
    busniess_List.append(entity)
    return entity


if __name__ == '__main__':
    # app.run(debug=True)
    run(host='localhost', port=8080)
