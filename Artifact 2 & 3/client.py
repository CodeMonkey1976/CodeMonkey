import requests
import pymongo
import json

# URL = http://localhost:8080/read?business_name="ACME TEST INC."

connection = pymongo.MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']


# return json.loads(json.dumps(string, indent=4, default=json_util.default))


# Retrieve Details Builder
def retrieve_details(ticker, details):
    URL = 'http://localhost:8080/retreiveDetails?ticker=' + ticker + "&details=" + details
    r = requests.get(URL)    
    return r.text

#Sector Search Builder
def sectorSearch(industry):
    industry = industry.replace('&', '$AND$')
    URL = 'http://localhost:8080/sectorSearch?industry=' + industry
    r = requests.get(URL)    
    print(r.content)
    
#String Search Builder 
def stringSearch(industry):
    industry = industry.replace('&', '$AND$')
    URL = 'http://localhost:8080/industrySearch?industry=' + industry
    r = requests.get(URL)    
    print(r.content)
    

#search High Low Builder
def searchHighLow(low, high):
    URL = 'http://localhost:8080/highLow?low=' + str(low) + '&high=' + str(high) 
    r = requests.get(URL)    
    print("The number of stocks between " + str(low) + " and " + str(high) + " is :" + str(r.json()))

    
#Update Entry in Mongo
def updateEntry(stock_ticker, stock_price):
    URL = 'http://localhost:8080/updateEntry?stock_ticker=' + stock_ticker + '&stock_price=' + stock_price 
    r = requests.get(URL)
    print(r.text)

#Create Entry in Mongo
def createEntry(stock_ticker, stock_price):
    URL = 'http://localhost:8080/createEntry?stock_ticker=' + stock_ticker + '&stock_price=' + stock_price 
    r = requests.get(URL)
    print(r.text)
    
# Delete Entry in Mongo    
def deleteEntry(stock_ticker):
    URL = 'http://localhost:8080/deleteStock?stock_ticker=' + stock_ticker
    r = requests.get(URL)
    print(r.text)
    

#Read Entry in Mongo
# Method allows user to download company data based off of Ticker
# Data will be displayed to the screen in json format
def readEntry(stock_ticker):
    URL = 'http://localhost:8080/getStock?stock_ticker=' + stock_ticker
    
    # User is asked if they would like to save the data as a file.
    menu = "UNKNOWN"
    file_name = None
    
    #While loop will only take "Y" or "N" in either lower or upper case
    while menu != "Y" and menu != "N":
      menu = input("Save File Y/N?\n")
      menu = menu.upper()
      
      if menu == "Y":
       # The the information is saved as a file, the user is asked for the file name
       # If the user does not give an extention of .txt then one is given  
        file_name = input("Please enter file name. *.txt\n").lower()   
        if file_name.find('.txt') < 1:
          file_name = file_name + ".txt"
    r = requests.get(URL)
  
    try:
      data = r.json()
      # If the file_name is not None then the user is saving the information to file_name
      # information is saved into the file of the user's choosing
      if file_name != None:
        print("\nWriting file...")
        file_name = open(file_name, "w")
        json.dump(data, file_name, ensure_ascii=False)
        file_name.close()
        print("\nWriting Complete.")

      # Display's data to screen in either case
      print(data)
        
    except:
        print(r.text)
        print("Error")
        
# MENUS        
        
#Details Menu
#Allow the user to retreive details about a Company using the Stock Ticker
#Menu cycles through detailList using plus and minus keys
#  
def detailsMenu():
  ticker = "T"  # Defined Default Company to AT&T because the developer is biased
  x = 0 # pointer for detailList
  detailList = [
        "Profit Margin",
        "Institutional Ownership",
        "EPS growth past 5 years",
        "Total Debt/Equity",
        "Current Ratio",
        "Return on Assets",
        "Sector",
        "P/S",
        "Change from Open",
        "Performance (YTD)",
        "Performance (Week)",
        "Quick Ratio",
        "Insider Transactions",
        "P/B",
        "EPS growth quarter over quarter",
        "Payout Ratio",
        "Performance (Quarter)",
        "Forward P/E",
        "P/E",
		    "200-Day Simple Moving Average",
        "Shares Outstanding",
        "Earnings Date",
        "52-Week High",
        "P/Cash",
        "Change",
        "Analyst Recom",
        "Volatility (Week)",
        "Country",
        "Return on Equity",
        "50-Day Low",
        "Price",
        "50-Day High",
        "Return on Investment",
        "Shares Float",
        "Dividend Yield",
        "EPS growth next 5 years",
        "Industry",
        "Beta",
        "Sales growth quarter over quarter",
        "Operating Margin",
        "EPS (ttm)",
        "PEG",
        "Float Short",
		    "52-Week Low",
        "Average True Range",
        "EPS growth next year",
        "Sales growth past 5 years",
        "Company",
        "Gap",
        "Relative Volume",
        "Volatility (Month)",
        "Market Cap",
        "Volume",
        "Gross Margin",
        "Short Ratio",
        "Performance (Half Year)",
        "Relative Strength Index (14)",
        "Insider Ownership",
        "20-Day Simple Moving Average",
        "Performance (Month)",
        "P/Free Cash Flow",
        "Institutional Transactions",
        "Performance (Year)",
        "LT Debt/Equity",
        "Average Volume",
        "EPS growth this year",
        "50-Day Simple Moving Average"
        ]
  while True:
    print("Details Menu\nDiscover Details about Company\n\n")
    print("1. Ticker = " + ticker + "." + detailList[x])
    print(" + = Advance List")
    print(" - = Go back")
    
    print("2. Get Details")
    print("9. Return Previous Menu")
    menu = input("Choice: ")
    if menu == "+":
      # Advance the list up one
      x = adjust_option(x, len(detailList) - 1, "+")

    if menu == "-":
      # Advance the list down one
      x = adjust_option(x, len(detailList) - 1, "-")
      
    if menu == str(1):
      # Allow user to change stock Ticker
      ticker = input("Enter Stock Ticker")
      ticker = ticker.upper()
    if menu == str(2):
      #Retrieve details from Mongo Server conserning Stock Ticker and details selected
      try:
        detail = retrieve_details(ticker, detailList[x])
        print("\n\n" + ticker + "." + detailList[x] + " = " + detail + "\n\n")
      except:
        print("\n\nError Communication with Server.\nCheck Information and try again")
      
    #Return to main menu
    if menu == str(9):
      break



#advance details sub menu option
# function controls the value of the x pointer for detailList
# Function does not allow x to be less than 0 or higher than 
# the length of the detail list
def adjust_option(x, max, direction):
  if direction == "+":
    x = x + 1
    if x > max:
      x = 0 
  else:
    x = x - 1
    if x < 0:
      x = max
  return x
    

# Aggregate  menu
# Allows user to lookup outstanding share in user defined industry
def aggregate_menu():
  industry = "Healthcare"  #Default Industry 
  while True:
      print("\n\nAggregate Menu")
      print("1. Sector Search = " + industry)
      print("2. Get Outstanding shares in " + industry + " industry")
      print("3. Get Details On Companies Menu")
      print("9. Return Previous Menu")
      menu = input("Choice: ")
      if menu == str(1):
        industry = input("Enter Sector Search : ")

      if menu == str(2):
        sectorSearch(industry)

      if menu == str(3):
        detailsMenu()

      # Go back one level in Menu Tree
      if menu == str(9):
        break
      


# High / low menu
# Allows user to search database 
def menuHighLow():
  low = 1
  high = 1
  industrySearch = "Medical Laboratories & Research"
  while True:
    print("\n\nDocument Retrieval")
    print("\n1. Low Number : " + str(low))
    print("2. High Number: " + str(high))
    print("3. Return Number of stocks beteen High / low")    
    print("4. Idustry Search: " + industrySearch)
    print("9. Return to Main Menu")
    menu = input("Choice: ")
    
    if menu == str(1):
      low = input("Low Number: ")
      
    if menu == str(2):
      high = input("High Number: ")
      
    if menu == str(3):
      searchHighLow(low, high)
      
    if menu == str(4):
      stringSearch(industrySearch)
      
    if menu == str(9):
      break
      
#search database for stocks within Range and sort by Return on Investment
def stock_range(low, high):
    URL = 'http://localhost:8080/stock_range?low=' + str(low) + '&high=' + str(high) 
    r = requests.get(URL)
    
    # create  company list array
    company_string_list = r.text
    company_list = []
    while company_string_list.find(" '''") > 0:
      end = company_string_list.find(" '''")
      company_list.append(company_string_list[0:end])
      company_string_list = company_string_list[end+4:]
    print("\n\nTop 10 Companies that fall into this range sorted 'Return on Investment' : \n")  
    for i in company_list:
      print(i)
      
  
#  Database Search for highest Return on Investment within stock range
def database_search(minimum_stock_price, maximum_stock_price):
  while True:
    print("\n\n Database Search Return on Investment within stock range")
    print("1.  Minimum Stock Value   =  " + str(minimum_stock_price))
    print("2.  Maximum Stock Value   =  " + str(maximum_stock_price))
    print("3.  Search Database ")
    print("9.  Return to Main Menu")
    menu = input("Choice: ")

    if menu == str(1):
      # Enter Minimum Stock Price
      while True:
        minimum_stock_price = input("Enter Minimum Stock Price : ")
        try:
          minimum_stock_price = int(minimum_stock_price) + 0
          break
        except:
          print("Please enter a number")

    elif menu == str(2):
      while True:
        # Enter Maximum Stock Price
        maximum_stock_price = input("Enter Maximum Stock Price : ")
        try:
          maximum_stock_price = int(maximum_stock_price) + 0
          break
        except:
          print("Please enter a number")

    elif menu == str(3):
      stock_range(minimum_stock_price, maximum_stock_price)

    elif menu == str(9):
      break

      
# main menu
def mainMenu():
  ticker = 'ARS'
  price = '20.00'
  while True:
    print("\n\n\nPlease Enter A selection")
    print("1.  Ticker = " + ticker)
    print("2.  Price  = " + str(price))
    print("3.  Update Ticker Price")
    print("4.  Document Retrieval")
    print("5.  Aggregate Menu")
    print("6.  Create Ticker Entry: ")
    print("7.  Display / Save Ticker Data " + ticker)
    print("8.  Delete Ticker: " + ticker)
    print("9.  Database Search Menu")
    print("10. Quit ")
    menu = input("Choice: ")
    
    if menu == str(1):
        ticker = input("Enter Stock Ticker: ")
        ticker = ticker.upper()
        price = 0.00

    if menu == str(2):
        price = input("Enter Stock Price: ")
        
    if menu == str(3):
        updateEntry(ticker, price)
        
    if menu == str(4):
          menuHighLow()
        
    if menu == str(5):
      aggregate_menu()
        
    #Create Ticker In database
    if menu == str(6):
        createEntry(ticker, price)

    if menu == str(7):
        readEntry(ticker)
        
    # Delete Ticker from Database
    if menu == str(8):
        deleteEntry(ticker)
        
    # Database Search for Best Investment
    if menu == str(9):
        database_search(0, 100)

    # Exit Program
    if menu == str(10):
        break
    

mainMenu()
