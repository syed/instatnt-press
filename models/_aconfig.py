# -*- coding: utf-8 -*-
#
# Instant Press. Instant sites. CMS developed in Web2py Framework
# Site: http://www.instant2press.com 
#
# Copyright (c) 2010 Mulone, Pablo Martín 
#
# License Code: GPL, General Public License v. 2.0
# License Content: Creative Commons Attribution 3.0 
#
# Also visit: www.web2py.com 
#             or Groups: http://groups.google.com/group/web2py 
#                http://groups.google.com/group/web2py-usuarios  
#
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>


################################
#### SETTINGS   ################
################################
#Important constants

IS_FIRST_TIME = True #this is the first time create default data, 
                     #after the first run, put this to False to reduce innecesary overheat 
IS_DEMO = False #fill some content, for testing pourpose, put to False in production
DB_CONNECT_URI = 'sqlite://storage.sqlite'
                 #mysql://username:password@localhost/test
                 #postgres://username:password@localhost/test


#In GAE this is not used, the admin is the admin of the application account
#Change this.
DEFAULT_ADMIN_FIRST_NAME = "John"
DEFAULT_ADMIN_LAST_NAME = "Doe" 
DEFAULT_ADMIN_EMAIL = "admin@mail.com" 
DEFAULT_ADMIN_PASSWORD = "admin123" 
DEFAULT_GROUPADMIN = "Admin" 

#RESPONSE VARS
RESPONSE_TITLE = "Instant Press - Instant sites"
RESPONSE_SUBTITLE = "Welcome to Instant Press"
RESPONSE_KEYWORDS = "Instant Press, Python, Web2py, Blog, CMS, Appengine, GAE"
RESPONSE_DESCRIPTION = '''Instant Press - Instant sites - 
                          Instant Press is a CMS system developed in Web2py Framework. 
                          Instant Press is simple, easy to use and attractive.'''
RESPONSE_AUTHOR = 'Martin Mulone'
RESPONSE_GENERATOR = 'Web2py Enterprise Framework'
RESPONSE_COPYRIGHT = 'Copyright (C) 2010 by Martin Mulone'

################################
# REGISTER settings   ##########
######################
## REGISTER_METHOD:
## ----------------
## 'Disabled' : Nobody can register
## 'Verification': Verification here mean: mail verification
## 'Approval': Approval need an admin approval
## 'Recaptcha': Recaptcha verify that is not a bot?
## 'None': No verification, never use in production
##
REGISTER_METHOD = 'None'
REGISTER_HMAC_KEY = 'sha512:ab9bf8b0-66f2-479a-bfbe-6de731c8fc75' #change some numbers 

#Recaptcha settings
RECAPTCHA_PUBLIC_KEY = 'PUBLIC_KEY' 
RECAPTCHA_PRIVATE_KEY = 'PRIVATE_KEY' 

#Mail
MAIL_SERVER = 'logging' #mail.settings.server = 'gae' #page360
MAIL_SENDER = 'you@gmail.com'
MAIL_LOGIN = 'username:password'


################################
# COMMENTS settings   ##########
################################
## COMMENTS_METHOD:
## ----------------
## 'Disabled': This disabled the comments, nothing show.
## 'Enabled':  This enabled local comments way.
## 'Disqus': This enabled comments via disqus.
COMMENTS_METHOD = 'Enabled'

################################
# COMMENTS settings   ##########
################################
## COMMENTS_REPLY_METHOD:
## ----------------
## 'Disabled': Nobody can reply.
## 'Register': You need a valid user to make a reply
COMMENTS_REPLY_METHOD = 'Register'

##########################
## Addthis, username of your account
## from: www.addthis.com
##
ADD_THIS_ENABLED = True
ADD_THIS_USERNAME = 'xa-4c8122cc5dbbd943' #change this to your user account.

###########################
## Disqus
## visit: www.disqus.com
## and register
DISQUS_SITE = "yoursiteid" #the site id you created on disqus
DISQUS_DEVELOPER = False #Put to true if you want to test in your local machine

############################################
## Less important constants here   #########
############################################
CACHE_TIME_EXPIRE_JSON = 60
CACHE_TIME_EXPIRE_PAGES = 60
DISABLE_THUMBNAIL = False #disable the generation of thumbnails, 
                          #you are not going to see thumbnails, but full image is ok!. 
                          #Disable if you have problem with PIL. 

STATIC_CSS = False #Put to true, if you are designing an style, this load from file 
                  #static/layouts. On False load from style db
CONTROLLER_ADMIN = "siteadmin"
CONTROLLER_DEFAULT = "default"

AVATAR_ENABLED = True
AVATAR_MAX_SIZE = 160 #pixels show in profile and store
AVATAR_SIZE = 48 #32 pixels is the pixels show in comments
THUMBNAIL_SIZE = 64 # 64 pixels
IMAGE_MAX_SIZE = 800 #800 pixels
UPLOAD_MAX_SIZE = 1600 #maximum pixel size of the upload image, yes if you have more pixels 
                        #than this you have to resize before.

#some style things and widgets
WIDGETS_AJAX = True
LIST_POST_IN_INDEX = True
FRONT_ENABLED = True
ABOUT_ENABLED = True
ARCHIVE_ENABLED = True
PAGES_ENABLED = True
TAGS_ENABLED = True
SEARCH_ENABLED = True
LAST_POST_ENABLED = True
CATEGORIES_ENABLED = True
FEED_ENABLED = True

#################################
### 'CKeditor'
### 'elRTE' #Experimental now not working dont use it
EDITOR = 'CKeditor'

#################################
### 'Markdown': The default one
### 'Markmin': Support the markmin language
EDITOR_LANGUAGE = 'Markdown' #these are experimental make no changes 

#################################
### Syntax highlighter
### http://alexgorbatchev.com/SyntaxHighlighter/
###
SYNTAX_HIGHLIGHT = False

#################################
## Fast Download
FAST_DOWNLOAD = True #fast download is a faster implementation of download,
                     #because not check auth

#################################
## Short url
## If you want http://www.mysite.com/blog/2010/10/10/my-article instead of http://www.mysite.com/blog/default/post/2010/10/10/my-article
## You have to edit routes.py in web2py to have this working
## Add this line:
## (r'.*:/instantpress/(?P<any>(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01]).*)$',r'/instantpress/default/post/\g<any>')
## 
SHORT_URL = False 

#################################
### GA Google analytics
GA_ENABLED = False #put to true if you want analytics
GA_ID = 'UA-XXXXX-X' #change the UA-XXXXX-X to be your site's ID

##################################
### LANGUAGE SUPPORT
### 'en' english
### 'es-es' spanish - español
### 'pt-br' portuguese - brazil
### 'nl' dutch
LANGUAGE_FORCE = False
LANGUAGE = 'en'

##################################
### AUTO_RESIZE_IMAGE:
### 
### If its enabled, this resize the image of uploaded file, and save as jpeg format
### the problem is, if you upload an png, you are going to have a resize jpeg forma.
AUTO_RESIZE_IMAGE = False





