import csv
import httplib2
from apiclient.discovery import build
import urllib
import json
import matplotlib.pyplot as plt 
import pickle




# This API key is provided by google as described in the tutorial
API_KEY = 'AIzaSyDHl9YPYoOL2rUgdF9oDQAO6OYuNUA0Uvo'

# This is the table id for the fusion table
TABLE_ID = '19Y7KxZmnKDhI_qqZxdaTkjckDgvqWhUYrxyLnnY'

try:
    fp = open("data.json")
    response = json.load(fp)
except IOError:
    service = build('fusiontables', 'v1', developerKey=API_KEY)
    query = "SELECT Age, OutcomeType FROM " + TABLE_ID + " WHERE AnimalType = 'DOG'"
    response = service.query().sql(sql=query).execute()
    fp = open("data.json", "w+")
    json.dump(response, fp)


summary = {} # this will be our summary of the data
columns = response['columns'] # the names of all columns
rows = response['rows'] # the actual data 

for i in range(0, len(columns)):  # loops through each column

    answers = {} # will store unique values for this column

    for row in rows:
        key = row[i] 
        # convert any string values to ascii, and any empty strings 
        # to a string called 'EMPTY' we can use as a key
        if type(key) is unicode: key = row[i].encode('ascii','ignore') 
        if key == '': key = 'EMPTY'
       
            
        try:               # increase the count the key already exists
            answers[key] = answers[key] + 1
        except KeyError:   # or set it to 1 if it does not exist
           answers[key] = 1
        summary[columns[i]] = answers   # store the result in summary

afile = open(r'd.pkl', 'wb')
pickle.dump(summary, afile)
afile.close()
    


