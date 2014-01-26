#!/usr/bin/env python
#
# Byte 2 Version 2
# 
# Copyright 11/2013 Jennifer Mankoff
#
# Licensed under GPL v3 (http://www.gnu.org/licenses/gpl.html)
#

# standard imports you should have already been using
import webapp2
import logging
from webapp2_extras import jinja2
import urllib

# this library is for decoding json responses
from webapp2_extras import json

# this is used for constructing URLs to google's APIS
from apiclient.discovery import build

# this library is for making http requests and so on
import httplib2

import json
import csv





# This API key is provided by google as described in the tutorial
API_KEY = 'AIzaSyDHl9YPYoOL2rUgdF9oDQAO6OYuNUA0Uvo'

# This is the table id for the fusion table
TABLE_ID = '19Y7KxZmnKDhI_qqZxdaTkjckDgvqWhUYrxyLnnY'

# This uses discovery to create an object that can talk to the 
# fusion tables API using the developer key
service = build('fusiontables', 'v1', developerKey=API_KEY)

# Use this url to find the data structure returned in your column query
# https://www.googleapis.com/fusiontables/v1/tables/TABLE_ID/columns?key=API_KEY

# we are adding a new class that will 
# help us to use jinja. MainHandler will sublclass this new
# class (BaseHandler), and BaseHandler is in charge of subclassing
# webapp2.RequestHandler 
class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

        # This will call self.response.write using the specified template and context.
        # The first argument should be a string naming the template file to be used. 
        # The second argument should be a pointer to an array of context variables
        #  that can be used for substitutions within the template
    # lets jinja render our response
    def render_response(self, _template, context):
        values = {'url_for': self.uri_for}

        logging.info(context)
        values.update(context)
        self.response.headers['Content-Type'] = 'text/html'

        # Renders a template and writes the result to the response.
        try: 
            rv = self.jinja2.render_template(_template, **values)
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            self.response.write(rv)
        except TemplateNotFound:
            self.abort(404)


# Class MainHandler now subclasses BaseHandler instead of webapp2
class MainHandler(BaseHandler):
         # This method should return the html to be displayed
    def get(self): 

        context = {}

#        request = service.column().list(tableId=TABLE_ID)
#        data = json.loads(str(request))
#        for k, v in data['items']:
#           logging.info(k + ' --> ' + v)

#        query = "SELECT * FROM " + TABLE_ID + " WHERE  AnimalType = 'DOG' LIMIT 10"
#        response = service.query().sql(sql=query).execute()
#        logging.info(response)


        # and render the response
        self.render_response('index.html', context) 


app = webapp2.WSGIApplication([('/.*', MainHandler)], debug=True)




