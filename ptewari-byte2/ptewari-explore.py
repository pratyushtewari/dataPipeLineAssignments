import csv
import httplib2
from apiclient.discovery import build
import urllib
import json
import matplotlib.pyplot as plt 



# This API key is provided by google as described in the tutorial
API_KEY = 'AIzaSyDHl9YPYoOL2rUgdF9oDQAO6OYuNUA0Uvo'

# This is the table id for the fusion table
TABLE_ID = '19Y7KxZmnKDhI_qqZxdaTkjckDgvqWhUYrxyLnnY'

try:
    fp = open("data.json")
    response = json.load(fp)
except IOError:
    service = build('fusiontables', 'v1', developerKey=API_KEY)
    query = "SELECT * FROM " + TABLE_ID + " WHERE AnimalType = 'DOG'"
    response = service.query().sql(sql=query).execute()
    fp = open("data.json", "w+")
    json.dump(response, fp)


summary = {} # this will be our summary of the data
columns = response['columns'] # the names of all columns
rows = response['rows'] # the actual data 

# we'll ignore some columns 
ignore = [u'Outcome', u'AnimalID', u'AnimalType', u'Name', u'IconName', u'IntakeDate', u'OutcomeDate', u'Latitude', u'Longitude', u'Breed']

for i in range(0, len(columns)):  # loops through each column
    if columns[i] in ignore: continue 

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

# some of the data is numeric -- especially the latituted, longitude,
# zipfound, and zipplaced. You might also explore the data
# about, for example, month found/placed numerically (are some months
# likely to have more strays or placements than others?). You could
# even parse the date data and look at for example the impact of 
# day of week. The code below shows some ways of visualizing 
# latitude and longitude only. 

plotdata = {} 
latitude = summary['ZipWherePlaced']
for i in latitude.keys():
    plotdata[float(i)] = latitude[i]

print plotdata

# make a bar plot of all the latitudes we found
plt.bar(plotdata.keys(), plotdata.values())
plt.show()

# you may want to explore other visualizations
# such as a histogram or other aspects of the data 
# including other columns


