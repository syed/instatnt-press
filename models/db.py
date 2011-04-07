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


def connect_to_db(config):
    
    if request.env.web2py_runtime_gae:
        
        from gluon.contrib.gae_memcache import MemcacheClient
        from gluon.contrib.memdb import MEMDB
        cache.memcache = MemcacheClient(request)
        cache.ram = cache.disk = cache.memcache
        
        db = DAL('gae')
        session.connect(request,response,MEMDB(cache.memcache))    
        
    else:                             
        
        db = DAL(config.connect_uri)
    
    return db


def init_mail(config):
    
    from gluon.tools import Mail
    
    mail = Mail()                                  # mailer
    mail.settings.server = config.mail_server or 'smtp.gmail.com:587'  # your SMTP server
    mail.settings.sender = config.mail_sender         # your email
    mail.settings.login = config.mail_login      # your credentials or None
    
    return mail


def init_auth(globals, db, config):
    
    from gluon.tools import Auth    
    import datetime
    
    #8.1.4 Customizing Auth page 350
    auth = Auth(globals,db)      #authentication/authorization
    auth.settings.hmac_key = config.register_hmac  # before define_tables()
    
    if config.register_method in ['Disabled']:
        auth.settings.actions_disabled.append('register') #disable register
    
    #Recaptcha (pag349)
    if config.register_method in ['Recaptcha']:
        from gluon.tools import Recaptcha
        auth.settings.captcha = Recaptcha(request, config.recaptcha_public, config.recaptcha_private)    

    
    db.define_table(
        auth.settings.table_user_name,
        Field('first_name', length=128, default=''),
        Field('last_name', length=128, default=''),
        Field('email', length=128, default='', unique=True),
        Field('password', 'password', length=512,
              readable=False, label='Password'),
        Field('registration_key', length=512,
              writable=False, readable=False, default=''),
        Field('reset_password_key', length=512,
              writable=False, readable=False, default=''),
        Field('registration_id', length=512,
              writable=False, readable=False, default=''),
        Field('created_on', 'datetime', default=datetime.datetime.today(),
                  writable=False,readable=False),                
        Field('site_language', length=128,writable=False, readable=False, 
              default='', label=T('Language')),                                                                                                            
        migrate=config.is_first_time 
        )
    
    custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
    custom_auth_table.first_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
    custom_auth_table.last_name.requires =  IS_NOT_EMPTY(error_message=auth.messages.is_empty)
    custom_auth_table.password.requires = [CRYPT(key=auth.settings.hmac_key)]
    custom_auth_table.email.requires = [
      IS_EMAIL(error_message=auth.messages.invalid_email),
      IS_NOT_IN_DB(db, custom_auth_table.email)]
    
    auth.settings.table_user = custom_auth_table

    auth.define_tables()         # creates all needed tables
    auth.settings.mailer = mail  # for user email verification
    
    if config.register_method in ['None','Recaptcha','Approval']:
        auth.settings.registration_requires_verification = False
    else:
        auth.settings.registration_requires_verification = True
    
    if config.register_method in ['Approval']:
        auth.settings.registration_requires_approval = True
    else:
        auth.settings.registration_requires_approval = False
    
    auth.settings.reset_password_requires_verification = True
        
    auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+\
        URL(r=request,c='default',f='user',args=['verify_email'])+\
        '/%(key)s to verify your email'
    auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+\
        URL(r=request,c='default',f='user',args=['reset_password'])+\
        '/%(key)s to reset your password'

    return auth


def get_login_panel():
    
    login_panel = ""
    
    if 'auth' in globals():
        if not auth.is_logged_in():
            link_register_caption = T('Register')
            link_register = A(link_register_caption, \
                              _href=URL(request.application,\
                                        i2p.config.controller_default,\
                                        'user/register'))
            link_login_caption = T('Sign in')
            link_login = A(link_login_caption, _href=auth.settings.login_url)        
            caption_notloggin = T('You are not logged in')                     
            login_panel = '''<div id="login-panel">%s %s | %s </div>''' % \
                            (caption_notloggin, link_login, link_register)
        else:
            #auth.user.email
            link_user = A(T('My Profile'), _href=URL(request.application,\
                                                     i2p.config.controller_default,\
                                                     'user/profile'))
            link_changepass_caption = T('Change password')
            link_changepass = A(link_changepass_caption, \
                                _href=URL(request.application,i2p.config.controller_default,\
                                          'user/change_password'))
            link_logout_caption = T('Logout')
            link_logout = A(link_logout_caption, _href=URL(request.application,\
                                                           i2p.config.controller_default,\
                                                           'user/logout'))
            login_panel = '<div id="login-panel">%s | %s | %s</div>' % \
                        (link_user, link_changepass, link_logout)
            
            
    return login_panel


if i2pConfig.language_force:
    T.force(i2pConfig.language)

db = connect_to_db(i2pConfig) #connect to database
mail = init_mail(i2pConfig) #initialize mail
auth = init_auth(globals(), db, i2pConfig) #initialize auth
i2p = Instant2Press(globals(), db, i2pConfig) #main class

#we need some information in the database to work correctly, 
#this fill with default information, the first time.
if i2pConfig.is_first_time:   
        
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules    
    
    if i2p.siteinfo.no_info_in_db(): #if there are no info in db, so i think is the first time 
                                        #and create default values                
        i2p.load_mod_filldb()
                
        i2p.filldb.info_default() #if it is the first time then fill with default values
    
        i2p.filldb.required_admin() #we need an admin                                
        
        i2p.filldb.default_style() #we need a basic style
        
        if i2pConfig.is_demo:    
                             
            i2p.filldb.test_users() #ok some others guys to test admin users
            
            i2p.filldb.test_articles() #the test article
    
    else:
                     
        i2pConfig.set_first_time(False)
                                                        
                                                    
                                                       
