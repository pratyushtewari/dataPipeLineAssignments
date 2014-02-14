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
    query = "SELECT Age, OutcomeType FROM " + TABLE_ID + " WHERE AnimalType = 'DOG'"
    response = service.query().sql(sql=query).execute()
    fp = open("data.json", "w+")
    json.dump(response, fp)



# we'll ignore some columns 
#ignore = [u'Outcome', u'AnimalID', u'AnimalType', u'Name', u'IconName', u'IntakeDate', u'OutcomeDate', u'Latitude', u'Longitude', u'Breed', u'SpayNeuter', u'AnimalID', u'AnimalType', u'IntakeDate', u'IntakeYear', u'IntakeMonth', u'Name', u'Breed', u'Sex', 'Size', u'Color', u'IntakeType', u'OutcomeSubtype', u'ZipWhereFound', u'Latitude', u'Longitude', u'ZipWherePlaced', u'OutcomeDate', u'OutcomeYear', u'OutcomeMonth', u'IconName']



