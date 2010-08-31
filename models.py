# Copyright (c) 2010, Scott Ferguson
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the software nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY SCOTT FERGUSON ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL SCOTT FERGUSON BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
