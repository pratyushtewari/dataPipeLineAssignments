#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

# this is for parsing the feed from the yahoo pipes
import feedparser
import logging

# this is for displaying HTML
from webapp2_extras import jinja2

# this is for encoding the search terms
import urllib

# BaseHandler subclasses RequestHandler so that we can use jinja
class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

        # This will call self.response.write using the specified template and context.
        # The first argument should be a string naming the template file to be used. 
        # The second argument should be a pointer to an array of context variables
        #  that can be used for substitutions within the template
    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)


# Class MainHandler now subclasses BaseHandler instead of webapp2
class MainHandler(BaseHandler):
         # This method should return the html to be displayed
    def get(self):  

    	feed = feedparser.parse("http://pipes.yahoo.com/pipes/pipe.run?_id=f0682aded041b9cde752ad0c85896315&_render=rss&textinput1=dog")
        # GIZMODO http://pipes.yahoo.com/pipes/pipe.run?_id=674e4a1c7b697443330466a3e6b0c1fa&_render=rss

        # this sets up feed as a list of dictionaries containing information 
        # about the RSS feed using a for loop
        feed = [{"link": item.link, "title":item.title, "description" : item.description,  "thumbnail": item.author, "published":item.published} for item in feed["items"]]
        
        # this will eventually contain information about the RSS feed
        context = {"feed" : feed}

        # here we call render_response instead of self.response.write.
        self.render_response('index.html', **context)

    # here we handle the results of the form
    def post(self):

        # this retrieves the contents of the search term 
        terms = self.request.get('search_term')

        # and converts it to a safe format for use in a url 
        terms = urllib.quote(terms)

        # now we construct the url for the yahoo pipe created in our tutorial
        # (you will want to replace this with your own url), using the search 
        # terms provided by the user in the form
        
        feed = feedparser.parse("http://pipes.yahoo.com/pipes/pipe.run?_id=f0682aded041b9cde752ad0c85896315&_render=rss&textinput1=" + terms)
        # this sets up feed as a list of dictionaries containing information 
        feed = [{"link": item.link, "title":item.title, "description" : item.description,  "thumbnail": item.author, "published":item.published} for item in feed["items"]]

        # this sets up the context with the user's search terms and the search
        # results in feed
        context = {"feed": feed}

        # this sends the context and the file to render to jinja2
        self.render_response('index.html', **context)

app = webapp2.WSGIApplication([('/.*', MainHandler)], debug=True)




