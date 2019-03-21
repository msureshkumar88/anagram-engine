from google.appengine.api import users
from google.appengine.ext import ndb
from models.user import User


class UserController:
    @classmethod
    def get_user(cls, current_user):

        user = users.get_current_user()
        url = ''
        url_string = ''
        myuser = None;
        if user:
            url = users.create_logout_url(current_user.request.uri)
            url_string = 'Logout'
            myuser_key = ndb.Key('User', user.email())
            myuser = myuser_key.get()
            if myuser == None:
                myuser = User(id=user.email(), email=user.email())
                myuser.put()
        else:
            url = users.create_login_url(current_user.request.uri)
            url_string = 'login'

        data = {
            'url': url,
            'url_string': url_string,
            'user': myuser,
            'user_id':user.user_id()
        }
        return data

    @classmethod
    def get_current_user(cls):
        return users.get_current_user()
