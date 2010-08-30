from django.db import models

import urllib, urllib2

C2DM_URL = 'https://android.apis.google.com/c2dm/send'

class C2DMProfile(models.Model):
    deviceId = models.CharField(max_length = 64)
    registrationId = models.CharField(max_length = 64)
    collapseKey = models.CharField(max_length = 50)
    authToken = models.CharField(max_lenth = 100)

    def send_message(self, message):
        values = {
            'registration_id': self.registrationId,
            'collapse_key': self.collapseKey,
        }

        params = urllib.urlencode(values)
        request = urllib2.Request(C2DM_URL, params)
        request.add_header("Authorization", "GoogleLogin auth=%s" % self.authToken)

        # Make the request
        response = urllib2.urlopen(request)

    def __unicode__(self):
        return '%s' % self.deviceId
