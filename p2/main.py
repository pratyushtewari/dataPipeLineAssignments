#!/usr/bin/env python
#
# Byte 4 Version 1
# 
# Copyright 2/2014 Jennifer Mankoff
#
# Licensed under GPL v3 (http://www.gnu.org/licenses/gpl.html)
#

# standard imports
import webapp2
from google.appengine.api import files
from google.appengine.api import memcache
from apiclient.discovery import build
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from oauth2client.appengine import AppAssertionCredentials 
from django.utils import simplejson
import httplib2
import urllib

import logging

# import for checking whether we are running on localhost or remotely
import os

# make sure to add this to app.yaml too
from webapp2_extras import jinja2

# BigQuery API Settings
_PROJECT_NUMBER        = '143834072116' 

# Define your production Cloud SQL instance information. 
_DATABASE_NAME = 'publicdata:samples.natality'

logging.info("setting up credentials")
credentials = AppAssertionCredentials(scope='https://www.googleapis.com/auth/bigquery')
http        = credentials.authorize(httplib2.Http(memcache))
service     = build("bigquery", "v2", http=http)
logging.info("done setting up credentials")

# we are adding a new class that will 
# help us to use jinja. MainHandler will sublclass this new
# class (BaseHandler), and BaseHandler is in charge of subclassing
# webapp2.RequestHandler  
class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)
        
    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)

class MainHandler(BaseHandler):
    def get(self):
        """default landing page"""
        
        #====================================================================
        # Sample query for getting #births by state 
        #====================================================================    
        
        logging.info("running birth related queries")
        #query_string = 'SELECT state, count(*) FROM [{0}] GROUP by state;'.format(_DATABASE_NAME)
        query_string = "SELECT year, state, count(*) FROM [publicdata:samples.natality] where year is not null and state is not null GROUP by year, state;".format(_DATABASE_NAME)
        births = self.run_query(query_string, filename='data/PA2.json')

        # similar to the google SQL work we did in byte4, the stuff we 
        # care about is in rows
        rows = births[u'rows']
        _states = []
        for row in rows:
            year  = row[u'f'][0][u'v']
            state = row[u'f'][1][u'v']
            count = row[u'f'][2][u'v']
            _state = {'year':int(year),'state':unicode.encode(state), 'count':int(count)}
            _states = _states + [_state]            
        
        context = {"_states": _states}
        
        # and render the response
        self.render_response('index.html', **context)

    def post(self):
        
        #====================================================================
        # Sample query for getting #births by state 
        #====================================================================
        state_selected = self.request.get('input_state')
        
        logging.info("running birth related queries")
        logging.info("Selected state" + state_selected)
        #query_string = 'SELECT state, count(*) FROM [{0}] GROUP by state;'.format(_DATABASE_NAME)
        query_string = "SELECT mother_age, avg(weight_pounds),year,state, count(*) FROM [publicdata:samples.natality] where state=\'" + state_selected + "\' and  mother_age < 20 GROUP by mother_age, year, state order by mother_age desc;".format(_DATABASE_NAME)
        births = self.run_query(query_string, filename='data/PA2.json')

        # similar to the google SQL work we did in byte4, the stuff we 
        # care about is in rows
        rows = births[u'rows']
        _states = []
        for row in rows:
            mother_age  = row[u'f'][0][u'v']
            avg_weight  = row[u'f'][1][u'v']
            year  = row[u'f'][2][u'v']
            state = row[u'f'][3][u'v']
            count = row[u'f'][4][u'v']
            _state = {'mother_age':unicode.encode(mother_age), 'avg_weight':float(avg_weight), 'year':int(year), 'state':unicode.encode(state), 'count':int(count)}
            _states = _states + [_state]            
        
        context = {"_states": _states}
        
        # and render the response
        self.render_response('index.html', **context)    


    # run the query specified in query_string, but if local open filename instead
    def run_query(self, query_string, filename=None, timeout=10000):
        if (os.getenv('SERVER_SOFTWARE') and
            os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
            # set up the query 
            query = {'query':query_string, 'timeoutMs':timeout}
            logging.info(query)
            # service is the oauth2 setup that we created above
            jobCollection = service.jobs()
            # project number is the project number you should have 
            # defined in your app
            return jobCollection.query(projectId=_PROJECT_NUMBER,body=query).execute()
        else:
            # open the data stored in a file called filename
            logging.info("loading file")
            try:
                fp = open(filename)
                return simplejson.load(fp)
            except IOError:
                logging.info("failed to load file %s", filename)
                return None
            except TypeError:
                return None

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

