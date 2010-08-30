from django.db import models

import urllib, urllib2

C2DM_URL = 'https://android.apis.google.com/c2dm/send'
AUTH_TOKEN = 'PASTE_AUTH_TOKEN_HERE'

class C2DMProfile(models.Model):
    deviceId = models.CharField(max_length = 64)
    registrationId = models.CharField(max_length = 140)
    collapseKey = models.CharField(max_length = 50)

    def send_message(self, **kwargs):
        values = {
            'registration_id': self.registrationId,
            'collapse_key': self.collapseKey,
        }

        for key,value in kwargs.items():
            values['data.%s' % key] = value

        headers = {
            'Authorization': 'GoogleLogin auth=%s' % AUTH_TOKEN,
        }

        try:
            params = urllib.urlencode(values)
            request = urllib2.Request(C2DM_URL, params, headers)

            # Make the request
            response = urllib2.urlopen(request)
        except Exception, error:
            print error

    def __unicode__(self):
        return '%s' % self.deviceId
