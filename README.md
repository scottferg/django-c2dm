django-c2dm
=====

django-c2dm is a Django module for sending a push notification to an Android device 
using Cloud 2 Device Messaging.  It provides a model to store the necessary information
required to send a message through C2DM as well as several helper functions.

## Setup

Using django-c2dm is easy.  Add an AUTH_TOKEN field to your settings.py file with the
ClientLogin token for your push account.

You can retrieve the ClientLogin token for your push account via cURL:

    curl -X POST https://www.google.com/accounts/ClientLogin -d Email=ACCOUNT -d Passwd=PASSWORD -d accountType=HOSTED_OR_GOOGLE -d service=ac2dm

Just replace ACCOUNT and PASSWORD with the relevant information.  

Copy everything in the response following Auth= to get your AUTH_TOKEN value.
