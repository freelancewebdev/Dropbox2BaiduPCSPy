#Dropbox 2 Baidu PCS Py
Python based Dropbox to Baidu PCS Data Migration Script

##Introduction
Chinese based internet services provider giant [Baidu](http://www.baidu.com/) offers a cloud based file storage service very similar to that offered by [Dropbox](http://www.dropbox.com/) called [Baidu PCS](http://pan.baidu.com/ "Baidu Personal Cloud Service").  However, in contrast with the service from Dropbox, which maxes out at 16GB for their free tier, most of which one has to earn via referrals, Baidu's offering comes with a whopping 2TB of free storage space without requiring jumping through any promotional hoops to access all that storage.  Even though the service is exclusively offered in the Chinese language at this point, the service is very usable using their browser based interface with Chrome and it's translation facility.  Baidu also provides clients for all the major desktop and mobile platforms which even non-chinese speakers can figure out with a little trial and error.  In 2013, Baidu tentatively began to engage with Western based developers by providing an [English language entrance to their developer portal](http://developer.baidu.com/en/) which seems to suggest that English langauge support for their services may be on the way. Even if you don't find the service suitable for every day use, it is still a pretty attractive option for archiving older less frequently needed data given the massive free disk space allowance.  Those of you concerned with the data security implications of storing your information on Chinese controlled servers might want to consider how likely it is that Baidu will cooperate with the NSA.

This simple Python 2.6 script makes use of the API's provided by Dropbox and Baidu to allow you to automate the migration of data from Dropbox to Baidu.  While I am not primarily a Python developer and while I cannot and do not claim that it has been exhaustively tested, this script has been used successfully on Mac and Linux to transfer around 27GB of my own personal data, including all kinds and sizes of files from spreadsheets to MP4 videos, some with filenames which had accented characters (so it should be fully UTF-8 compliant).  You should note that currently it may need some adjustments to run on Windows - yet to be tested.  

It comes out of the box with some simple logging, noting the start and end times of the script's execution and listing files it had issues migrating.  I have also added some simple retry logic where required to handle brief network outages.  It takes care of the process of obtaining user authentication tokens itself, guiding the user as required. It only requires that you have a minimum few elements in place in advance to successfully use it.

1. A Dropbox account with data to migrate (doh)
2. A Dropbox application with credentials to use their API
3. A Baidu PCS account where your data will be stored.
4. A Baidu application with credentials and permissions to use their API
5. Installed script dependencies
6. A configured version of the Python script.

I will assume you already have a Dropbox account set up and configured, otherwise there wouldn't be much point in using this script.  See below for details on getting the other elements in place.

##Preperation
###Setting Up a Dropbox Application
To set up your Dropbox application, go to the [Dropbox developers portal](https://www.dropbox.com/developers) and log in with your Dropbox credentials if required.  From there, click the 'App Console' link on the left and choose to create a new Dropbox API app. Choose the files and datastores option under the data type your application needs to access, choose NOT to limit your app to its own folder and choose the option to allow your app to access all file types. Finally, choose a name for your app, preferably something meaningful, and you are done with your Dropbox application setup.  Just make a note of your App Key and App Secret as you will need them to configure the script in a bit.

###Setting Up a Baidu PCS Account
Unless you read Chinese, I would recommend you use the [Google Chrome Web Browser](http://www.google.com/chrome) to complete this series of steps to set up your Baidu PCS account as, as previously mentioned, it comes with built in web page translation.
Go to the [Baidu PCS Homepage](https://pan.baidu.com) and register using the button provided.  You can give either your email address OR a Chinese mobile number so most of you will probably give an email address, password and complete the captcha as required.  After submitting the registration form you will then be informed that you must activate your account fully by following the link sent to you via email.  Do so and your Baidu account is ready for storing your data.

###Setting Up Your Baidu Developer Account
Now that you have a Baidu account you may become a Baidu developer.  While logged in to your Baidu PCS account, simply head on over to the [Baidu Developer Portal](https://developer.baidu.com/) and choose the 'Registered Developer' link from the dropdown menu which appears when you hover over your username in the top navigation menu which will take you to the [Baidu Developer registration form](http://developer.baidu.com/user/reg).
The form is pretty self explanatory.  To complete it successfully you must supply your mobile phone number so that you can obtain the verification code required to complete the registration process - you should note that only one developer account can be created per phone number.  Once the registration process is complete you can proceed to set up your application.

###Setting up Your Baidu Application
This is probably the most challenging part of the process, simply because of the language difficulties and the effect that the Google Translator has on the layout of the pages in the Baidu Developer Application Management Console.  I will try to be as clear as possible.
If you haven't already, log into the [Baidu developer portal](https://developer.baidu.com/) using the credentials of the account you created above and then click on the 'Management Console' link in the top navigation menu which will lead you [here](http://developer.baidu.com/console#app/project).  Then click the 'Create Project' button which will take you to [this screen](http://developer.baidu.com/console#app/create) where you can proceed to configure your application.  The only thing you need to do on this screen is name your app something meaningful.

When you submit the name for your app, the resulting screen will give you your API Key and Secret Key and you should note those for later use in the script.

Also on this page you will notice a list of 'Developer Services' either above or to the left of your app details (depending on how Google Chrome renders the screen layout).  In order for your newly created app to function, you must explicitly obtain authorisation to use the PCS API.  It seems this authorisation is currently manually processed by Baidu.

Click on the 'Other API' link from the list of 'Developer Services'. First check the checkbox beside the PCS item in the resulting API list and then click on the 'Open' button at the top of the list.  When you do this, a popup window will appear with a short form which must be completed basically requiring you to enter the following details about your application in the 3 fields provided:

1. The folder name for your app
Unlike Dropbox, currently each app that uses the Baidu API is sandboxed to its own folder in the user's storage and cannot modify files outside this folder.  Usually you would name the folder after your app.  I recommend you stick to ASCII letters and digits only for the name.
2. A brief description of your app.  At this point I have submitted descriptions in both English and Chinese (via Google translate) and both apps were authorised without a hitch.  I basically said I was using the API for personal use and educational purposes.
3. You must provide 3 pieces of information in the last field:
...1. The estimated number of users of your app - in this case it will be only you so one would seem an appropriate answer.
...2. An estimate of the storage required - I basically doubled the space I had occupied on Dropbox as an estimate but implicitly said that this was only an estimate.
...3. An estimate of the traffic/bandwidth your user(s) will generate - I put this at 30GB monthly without issue.

Please note that sometimes the ability to 'Open' the PCS API authorisation is disabled temporarily but in my experience these outages do not last more than a couple of days, so if you find this facility disabled, check back regularly for changes.

Finally, click the 'Security Settings' button also in the 'Other API' screen at the tope of the API list.  Choose to DISABLE implicit grant authorisation in the resulting form and then click the 'Determine' button to submit your change - the implicit grant authorisation method is used by websites to obtain authorisation tokens to access their users' accounts but in this case we are using a device authorisation so the implicit grant process is not used and those details are not required.

###Installing Script Dependencies
You will need the [Baidu Python PCS](https://pypi.python.org/pypi/baidupcs/0.3.1) and the [Dropbox](https://www.dropbox.com/developers/core/sdks/python) modules.  Instructions for installing these modules on different platforms are discussed at each of the links provided and are beyond the scope of this project to provide.

###Configuring the Script
You should edit the config file Dropbox2BaiduPCS_sample.cfg adding your own values obtained above and the save the file as Dropbox2BaiduPCS.cfg in the same directory as you are runnig Dropbox2BaiduPCS.py.  The following values are required:

1. db\_app\_key: 
Your Dropbox app key obtained above (string)
2. db\_app\_secret
Your Dropbox app secret obtained above (string)
3. b\_app\_key: 
Your Baidu app key obtained above (string)
4. b\_app\_secret: 
Your Baidu app secret obtained above (string)
5. b\_folder: 
Your Baidu app folder name as configured on Baidu above.
6. db\_ignore\_folders: 
A comma separated list of folder names which you wish to ignore in your migration - paths 
including any of these names will be skipped.  If you do not wish to skip any folders you must provide an empty string, i.e. ignorefolders = ''. (string)
7. secure\_mode: 
By default this setting is false which means that once the script has obtained the access tokens to use the Dropbox and Baidu API's, it will store them in config file as plaintext.  On subsequent runs of this script, the access tokens will be read from these files and you will not have to go through the authentication process again.  However, storing these tokens is plain text is not very secure so you have the option of not persisting this information to disk by setting the 'secure_mode' configuration variable to True. (boolean)

###Running the Script
Just call python Dropbox2BaiduPCS.py

###Licensing
Copyright (C) 2014  Joe Molloy

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see http://www.gnu.org/licenses/.










