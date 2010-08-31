django-c2dm
=====

django-c2dm is a Django module for sending push messages to an Android device 
using Cloud 2 Device Messaging.  It provides a model to store the necessary information
required to send a message through C2DM as well as several helper functions.

## Setup

Using django-c2dm is easy.  Add the following line to your settings.py file: 

    C2DM_AUTH_TOKEN = 'YOUR_PUSH_ACCOUNT_AUTH_TOKEN'

Where YOUR_PUSH_ACCOUNT_AUTH_TOKEN is the ClientLogin token for your push account.

And then add django_c2dm to your INSTALLED_APPS.

## Finding your ClientLogin token

You can retrieve the ClientLogin token for your push account via cURL:

    curl -X POST https://www.google.com/accounts/ClientLogin -d Email=ACCOUNT -d Passwd=PASSWORD -d accountType=HOSTED_OR_GOOGLE -d service=ac2dm

Just replace ACCOUNT and PASSWORD with the relevant information.

Copy everything in the response following Auth= to get your AUTH_TOKEN value.

## Usage

To send a message to a device call send_message() on the model.  send_message() only needs kwargs as a parameter.
Use this to populate the data.X fields in your message.  These fields will be provided as extras on the intent
that the device receives.

You can also set the delay_while_idle parameter to True to enable this feature.
