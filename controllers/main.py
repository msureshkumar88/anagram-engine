import webapp2
from google.appengine.api import users
import os
import logging
import template_engine

from models.anagram import Anagram
from library.helper import Helper


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        # URL that will contain a login or logout link
        # and also a string to represent this
        url = ''
        url_string = ''
        # pull the current user from the request
        user = users.get_current_user()
        # aaa = Anagram(tags = ["abc","abc","abc","abc"], ena_count = len(["abc","abc","abc","abc"]))
        # aaa.put()

        #logging.info(Helper.get_word_key("asdsadssdsd"))
        Helper.validate_string("abcAAA")
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user
        }

        # pull the template file and ask jinja to render
        # it with the given template values
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/home.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
