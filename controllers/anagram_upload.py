import webapp2
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import logging

class AnagramUpload(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        logging.info(self.get_uploads())
        upload = self.get_uploads()[0]
        blob_reader = blobstore.BlobReader(upload.key())
        logging.info(blob_reader.read())
        blobstore.delete(upload.key())
        #
        # self.redirect('/view_photo/%s' % upload.key())

app = webapp2.WSGIApplication([
    ('/upload_text', AnagramUpload)
], debug=True)
