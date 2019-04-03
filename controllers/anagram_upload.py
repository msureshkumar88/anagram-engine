import webapp2
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import logging
from library.helper import Helper
from library.user import UserController


class AnagramUpload(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        user = UserController.get_user(self)
        logging.info(self.get_uploads())
        upload = self.get_uploads()[0]
        blob_reader = blobstore.BlobReader(upload.key())
        # only allow to upload valid words
        for val in blob_reader.readlines():
            val = val.rstrip()
            if Helper.validate_string(val):
                Helper.saveAnagram(val,user['user'].email)
        blobstore.delete(upload.key())
        self.redirect('/anagram/upload')

app = webapp2.WSGIApplication([
    ('/upload_text', AnagramUpload)
], debug=True)
