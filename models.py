from django.db import models
from django.conf import settings

import urllib, urllib2

C2DM_URL = 'https://android.apis.google.com/c2dm/send'

class C2DMProfile(models.Model):
    '''
    Profile of a c2dm-enabled Android device

    device_id - Unique ID for the device.  Simply used as a default method to specify a device.
    registration_id - Result of calling registration intent on the device. Subject to change.
    collapse_key - Required arbitrary collapse_key string.
    last_messaged - When did we last send a push to the device
    failed_push - Have we had a failure when pushing to this device? Flag it here.
    '''
    device_id = models.CharField(max_length = 64)
    registration_id = models.CharField(max_length = 140)
    collapse_key = models.CharField(max_length = 50)
    last_messaged = models.DateTimeField(blank = True, default = datetime.datetime.now)
    failed_push = models.BooleanField(default = False)

    def send_message(self, **kwargs):
        '''
        Sends a message to the device.  
        
        data.keyX fields are populated via kwargs.
        '''
        values = {
            'registration_id': self.registration_id,
            'collapse_key': self.collapse_key,
        }

        for key,value in kwargs.items():
            values['data.%s' % key] = value

        headers = {
            'Authorization': 'GoogleLogin auth=%s' % settings.AUTH_TOKEN,
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

def send_multiple_messages(self, device_list, **kwargs):
    '''
    Same as send_message but sends to a list of devices.

    data.keyX fields are populated via kwargs.
    '''
    for device in device_list:
        device.send_message(kwargs)
