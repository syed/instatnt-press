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


class Config(object): 
    
    def __init__(self):
        pass
    
    def set_first_time(self, first_time):        
        self.is_first_time = first_time
    
    def set_is_demo(self, demo):
        self.is_demo = demo
    
    def set_connect_uri(self, uri):
        self.connect_uri = uri
    
    def set_first_name(self,first_name):
        self.first_name =  first_name
    
    def set_last_name(self, last_name):
        self.last_name = last_name
    
    def set_email(self, email):
        self.email = email
    
    def set_password(self, passw):
        self.passw = passw
    
    def set_group_admin(self, group_admin):
        self.group_admin = group_admin
    
    def set_register_method(self, method):
        self.register_method = method
    
    def set_register_hmac(self, hmac):
        self.register_hmac = hmac
    
    def set_recaptcha_public(self, key):
        self.recaptcha_public = key
    
    def set_recaptcha_private(self, key):
        self.recaptcha_private = key
    
    def set_mail_server(self, mail_server):
        self.mail_server =  mail_server
    
    def set_mail_sender(self, mail_sender):
        self.mail_sender = mail_sender
    
    def set_mail_login(self, mail_login):
        self.mail_login = mail_login
    
    def set_comments_method(self, method):
        self.comments_method = method
    
    def set_comments_reply(self, method):
        self.comments_reply = method
    
    def set_addthis_enabled(self, enabled):
        self.addthis_enabled = enabled
        
    def set_addthis_user(self, user):
        self.addthis_user = user
    
    def set_disqus_site(self, site):
        self.disqus_site = site
    
    def set_disqus_dev(self, dev):
        self.disqus_dev = dev
    
    def set_controller_admin(self, admin):
        self.controller_admin = admin
    
    def set_controller_default(self, default):
        self.controller_default = default  
        
    def set_widgets_ajax(self, ajax):
        self.widgets_ajax = ajax
    
    def set_avatars_enabled(self, avatars):
        self.avatars_enabled = avatars 
    
    def set_list_post_in_index(self, enabled):
        self.list_post_in_index = enabled  
        
    def set_front_enabled(self, enabled):
        self.front_enabled = enabled
    
    def set_about_enabled(self, enabled):
        self.about_enabled = enabled  
    
    def set_archive_enabled(self, enabled):
        self.archive_enabled = enabled   
    
    def set_pages_enabled(self, enabled):
        self.pages_enabled = enabled
    
    def set_tags_enabled(self, enabled):
        self.tags_enabled = enabled 
        
    def set_search_enabled(self, enabled):
        self.search_enabled = enabled  
    
    def set_last_post_enabled(self, enabled):
        self.last_post_enabled = enabled
    
    def set_categories_enabled(self, enabled):
        self.categories_enabled = enabled
    
    def set_feed_enabled(self, enabled):
        self.feed_enabled = enabled
    
    def set_avatar_max_size(self, size):
        self.avatar_max_size = size
    
    def set_avatar_size(self, size):
        self.avatar_size = size
    
    def set_thumbnail_size(self, size):
        self.thumbnail_size = size
    
    def set_image_max_size(self, size):
        self.image_max_size = size
    
    def set_upload_max_size(self, size):
        self.upload_max_size = size  
    
    def set_static_css(self, isstatic):
        self.static_css = isstatic
    
    def set_editor(self, editor):
        self.editor = editor
    
    def set_editor_language(self, language):
        self.editor_language = language
    
    def set_syntax_highlight(self, highlight):
        self.syntax_highlight = highlight
    
    def set_fast_download(self, download):
        self.fast_download = download
    
    def set_short_url(self, is_short):
        self.short_url = is_short
        
    def set_ga_enabled(self, enabled):
        self.ga_enabled = enabled
        
    def set_ga_id(self, id):
        self.ga_id = id
        
    def set_language(self, language):
        self.language = language
        
    def set_language_force(self, force):
        self.language_force = force
    
    def set_auto_resize_image(self, resize_image):
        self.auto_resize_image = resize_image
    
    def set_fulltext_field(self):        
        #This is to preserve compatibility
        #the problem is that I can not use field fulltext in mysql, because i don't know that,
        #so in mysql I use full_text instead of fulltext.
        connect_uri = self.connect_uri
        if connect_uri[:5]=='mysql':
            self.fulltext_field = 'full_text'
        else:
            self.fulltext_field = 'fulltext'

       

#check some values in constants

valid_method_register = ['Disabled','Verification','Approval','Recaptcha','None']
if REGISTER_METHOD not in valid_method_register:
    raise ValueError, "Not a valid method register"

valid_method_comments = ['Disabled','Enabled','Disqus']
if COMMENTS_METHOD not in valid_method_comments:
    raise ValueError, "Not a valid method comments"

valid_method_comments_reply = ['Disabled','Register']
if COMMENTS_REPLY_METHOD not in valid_method_comments_reply:
    raise ValueError, "Not a valid method reply comments"

IMG_SERVING_SIZES = [
          32, 48, 64, 72, 80, 90, 94, 104, 110, 120, 128, 144,
          150, 160, 200, 220, 288, 320, 400, 512, 576, 640, 720,
          800, 912, 1024, 1152, 1280, 1440, 1600] #this is from gae http://code.google.com/appengine/docs/python/images/functions.html#Image_get_serving_url 

IMG_SERVING_CROP_SIZES = [32, 48, 64, 72, 80, 104, 136, 144, 150, 160]

if AVATAR_SIZE not in IMG_SERVING_SIZES:
    raise ValueError, "Not a valid size of pixels use one of this %s " % '32, 48, 64, 72, 80, 90, 94, 104, 110, 120, 128 ... etc.'

if THUMBNAIL_SIZE not in IMG_SERVING_SIZES:
    raise ValueError, "Not a valid size of pixels use one of this %s " % '32, 48, 64, 72, 80, 90, 94, 104, 110, 120, 128 ... etc.'

if IMAGE_MAX_SIZE not in IMG_SERVING_SIZES:
    raise ValueError, "Not a valid size of pixels use one of this %s " % '32, 48, 64, 72, 80, 90, 94, 104, 110, 120, 128 ... etc.'

if UPLOAD_MAX_SIZE not in IMG_SERVING_SIZES:
    raise ValueError, "Not a valid size of pixels use one of this %s " % '32, 48, 64, 72, 80, 90, 94, 104, 110, 120, 128 ... etc.'

valid_editor = ['CKeditor','elRTE']
if EDITOR not in valid_editor:
    raise ValueError, "Not a valid editor"

valid_editor_language = ['Markdown','Markmin']
if EDITOR_LANGUAGE not in valid_editor_language:
    raise ValueError, "Not a valid editor language"


valid_language = ['en','es-es','pt-br','nl']
if LANGUAGE not in valid_language:
    raise ValueError, "Not a valid language or language is not supported"


i2pConfig = Config()
i2pConfig.set_first_time(IS_FIRST_TIME)
i2pConfig.set_is_demo(IS_DEMO)
i2pConfig.set_connect_uri(DB_CONNECT_URI)
i2pConfig.set_first_name(DEFAULT_ADMIN_FIRST_NAME)
i2pConfig.set_last_name(DEFAULT_ADMIN_LAST_NAME)
i2pConfig.set_email(DEFAULT_ADMIN_EMAIL)
i2pConfig.set_password(DEFAULT_ADMIN_PASSWORD)
i2pConfig.set_group_admin(DEFAULT_GROUPADMIN)
i2pConfig.set_register_method(REGISTER_METHOD)
i2pConfig.set_register_hmac(REGISTER_HMAC_KEY)
i2pConfig.set_recaptcha_public(RECAPTCHA_PUBLIC_KEY)
i2pConfig.set_recaptcha_private(RECAPTCHA_PRIVATE_KEY)
i2pConfig.set_mail_server(MAIL_SERVER)
i2pConfig.set_mail_sender(MAIL_SENDER)
i2pConfig.set_mail_login(MAIL_LOGIN)
i2pConfig.set_comments_method(COMMENTS_METHOD)
i2pConfig.set_comments_reply(COMMENTS_REPLY_METHOD)
i2pConfig.set_addthis_enabled(ADD_THIS_ENABLED)
i2pConfig.set_addthis_user(ADD_THIS_USERNAME)
i2pConfig.set_disqus_site(DISQUS_SITE)
i2pConfig.set_disqus_dev(DISQUS_DEVELOPER)
i2pConfig.set_controller_admin(CONTROLLER_ADMIN)
i2pConfig.set_controller_default(CONTROLLER_DEFAULT)
i2pConfig.set_widgets_ajax(WIDGETS_AJAX)
i2pConfig.set_avatars_enabled(AVATAR_ENABLED)
i2pConfig.set_list_post_in_index(LIST_POST_IN_INDEX)
i2pConfig.set_front_enabled(FRONT_ENABLED)
i2pConfig.set_about_enabled(ABOUT_ENABLED)
i2pConfig.set_archive_enabled(ARCHIVE_ENABLED)
i2pConfig.set_pages_enabled(PAGES_ENABLED)
i2pConfig.set_tags_enabled(TAGS_ENABLED)
i2pConfig.set_search_enabled(SEARCH_ENABLED)
i2pConfig.set_last_post_enabled(LAST_POST_ENABLED)
i2pConfig.set_categories_enabled(CATEGORIES_ENABLED)
i2pConfig.set_feed_enabled(FEED_ENABLED)
i2pConfig.set_avatar_max_size(AVATAR_MAX_SIZE)
i2pConfig.set_avatar_size(AVATAR_SIZE)
i2pConfig.set_thumbnail_size(THUMBNAIL_SIZE)
i2pConfig.set_image_max_size(IMAGE_MAX_SIZE)
i2pConfig.set_upload_max_size(UPLOAD_MAX_SIZE)
i2pConfig.set_static_css(STATIC_CSS)
i2pConfig.set_editor(EDITOR)
i2pConfig.set_editor_language(EDITOR_LANGUAGE)
i2pConfig.set_syntax_highlight(SYNTAX_HIGHLIGHT)
i2pConfig.set_fast_download(FAST_DOWNLOAD)
i2pConfig.set_short_url(SHORT_URL)
i2pConfig.set_ga_enabled(GA_ENABLED)
i2pConfig.set_ga_id(GA_ID)
i2pConfig.set_language(LANGUAGE)
i2pConfig.set_language_force(LANGUAGE_FORCE)
i2pConfig.set_auto_resize_image(AUTO_RESIZE_IMAGE)
i2pConfig.set_fulltext_field()


response.title = RESPONSE_TITLE
response.subtitle = RESPONSE_SUBTITLE
response.keywords = RESPONSE_KEYWORDS
response.description = RESPONSE_DESCRIPTION
response.meta.author = RESPONSE_AUTHOR
response.meta.description = RESPONSE_DESCRIPTION
response.meta.keywords = RESPONSE_KEYWORDS
response.meta.generator = RESPONSE_GENERATOR
response.meta.copyright = RESPONSE_COPYRIGHT

