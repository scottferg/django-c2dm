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
from django.db.models.signals import post_save

import urllib, urllib2
from urllib2 import URLError
import datetime

C2DM_URL = 'https://android.apis.google.com/c2dm/send'

class AndroidDevice(models.Model):
    '''
    Profile of a c2dm-enabled Android device

    device_id - Unique ID for the device.  Simply used as a default method to specify a device.
    registration_id - Result of calling registration intent on the device. Subject to change.
    collapse_key - Required arbitrary collapse_key string.
    last_messaged - When did we last send a push to the device
    failed_push - Have we had a failure when pushing to this device? Flag it here.
    '''
    device_id = models.CharField(max_length = 64, unique = True)
    registration_id = models.CharField(max_length = 140)
    collapse_key = models.CharField(max_length = 50)
    last_messaged = models.DateTimeField(blank = True, default = datetime.datetime.now)
    failed_push = models.BooleanField(default = False)

    def send_message(self, delay_while_idle = False, **kwargs):
        '''
        Sends a message to the device.  
        
        delay_while_idle - If included, indicates that the message should not be sent immediately if the device is idle. The server will wait for the device to become active, and then only the last message for each collapse_key value will be sent.
        data.keyX fields are populated via kwargs.
        '''
        if self.failed_push:
            return

        values = {
            'registration_id': self.registration_id,
            'collapse_key': self.collapse_key,
        }

        if delay_while_idle:
            values['delay_while_idle'] = ''

        for key,value in kwargs.items():
            values['data.%s' % key] = value

        headers = {
            'Authorization': 'GoogleLogin auth=%s' % settings.C2DM_AUTH_TOKEN,
        }

        try:
            params = urllib.urlencode(values)
            request = urllib2.Request(C2DM_URL, params, headers)

            # Make the request
            response = urllib2.urlopen(request)

            result = response.read().split('=')

            if 'Error' in result:
                if result[1] == 'InvalidRegistration' or result[1] == 'NotRegistered':
                    self.failed_push = True
                    self.save()

                raise Exception(result[1])
        except URLError:
            return false
        except Exception, error:
            return false 

    def __unicode__(self):
        return '%s' % self.device_id

def send_multiple_messages(device_list, **kwargs):
    '''
    Same as send_message but sends to a list of devices.

    data.keyX fields are populated via kwargs.
    '''
    for device in device_list:
        device.send_message(kwargs)

def filter_failed_devices():
    '''
    Removes any devices with failed registration_id's from the database
    '''
    for device in AndroidDevice.objects.filter(failed_push = True):
        device.delete()

def registration_completed_callback(sender, **kwargs):
    '''
    Returns a push response when the device has successfully registered.
    '''
    profile = kwargs['instance']
    profile.send_message(message = 'Registration successful', result = '1')
post_save.connect(registration_completed_callback, sender = AndroidDevice)
