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


import math
import datetime

from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *
from gluon.sql import *
import gluon.contrib.simplejson as sj

#local
from utils import *

ADMIN_USERS_LIST_PER_PAGE = 5
ADMIN_MAX_LIST_PAGES = 10


class Users(object): 
    
    def __init__(self, i2p):
        
        self.i2p = i2p 
        
    
    def get_user_title(self, id):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        if request.env.web2py_runtime_gae: 
            #in gae the user administrator is the only author.
            user_title = T("Site administrator")
        else:      
            user_title = T("Anonymous")
            
        users = db(db.auth_user.id == id).select()    
        if users:
            user = users[0]
            user_title = user.last_name + ", " + user.first_name    
        
        return user_title
    
    
    def is_user_an_admin(self):
        
        request = self.i2p.environment.request
        auth = self.i2p.environment.auth
        
        if request.env.web2py_runtime_gae:
            from google.appengine.api import users
            if users.is_current_user_admin():
                return True        
        else:
            if auth:
                if auth.is_logged_in():   
                    is_admin = auth.has_membership(auth.id_group(self.i2p.config.group_admin))
                    if is_admin:
                        return True    
        return False 
    
    #added support to gae admin users
    def check_credentials_is_admin(self):  
        
        request = self.i2p.environment.request
        auth = self.i2p.environment.auth
          
        is_an_admin = self.is_user_an_admin()
        if not is_an_admin:
            if request.env.web2py_runtime_gae:
                from google.appengine.api import users
                login_html = '<a href="%s">%s</a>.' \
                    % (users.create_login_url(request.env.path_info), \
                       T('Sign in with your google account'))
                raise HTTP(200, '<html><body>%s</body></html>' % login_html)
            else:
                next = auth.settings.on_failed_authorization
                redirect(next)
                
        return is_an_admin
               
                    
    #The user is logged in?
    def is_user_logged_in(self):
        
        logged_in=False
        auth = self.i2p.environment.auth
        
        if auth:
            if auth.is_logged_in():
                logged_in=True 
        
        return logged_in    
    
    
                
class admUsers(object): 
    
    def __init__(self, i2p):
        
        self.i2p = i2p 
        
           
    #ADMIN    
    def list(self, currentpage=1, search_text=""):        
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        auth = self.i2p.environment.auth
        
        if not isinstance(search_text, (unicode, str) ): 
            search_text = ""
            
            
        max_users=ADMIN_USERS_LIST_PER_PAGE
        max_display_pages=ADMIN_MAX_LIST_PAGES
        
        limit_inf = (max_users * currentpage) - max_users
        limit_sup = limit_inf + max_users 
        
        query = (db.auth_user.id>0) 
        if search_text!="":
            query = query & (db.auth_user.last_name.like(search_text+"%"))
        count_users = db(query).count()
        last_users = db(query).select(db.auth_user.ALL,\
                                      orderby=~db.auth_user.created_on,\
                                      limitby=(limit_inf, limit_sup))
                   
        link_register = A(T('Register'), \
                          _href=URL(request.application,\
                                    self.i2p.config.controller_default,\
                                    'user/register'), \
                          _style="padding-left: 5px;")  
        icon_register_url = URL(request.application,'static','images/toolbar_add.png')    
        toolbar_register_style = 'padding-left: 20px; background-image: url(%s); background-repeat: no-repeat;' \
                                % icon_register_url
        
        refresh_list = A(T("Refresh"), _href='javascript: void(0);', \
                         _onclick="UserList(1);" ,\
                         _title="%s"%T('Reload the list'))
        icon_refresh_url = URL(request.application,'static','images/toolbar_refresh.png')    
        toolbar_refresh_style = 'padding-left: 20px; background-image: url(%s); background-repeat: no-repeat;' \
                                % icon_refresh_url
        
        input_search = '<input type="text" id="input-search" style="width: 200px; height: 20px; margin: 0px;" />'
        icon_search_url = URL(request.application,'static','images/search.png')
        icon_search = IMG(_src=icon_search_url, _alt="search")
        do_search = A(icon_search, _href='javascript: void(0);', \
                      _onclick="UserSearch();" ,\
                      _title="%s"%T('Search in last name'))
            
        toolbar_register = '<li style="%s">%s</li>' % (toolbar_register_style,link_register.xml())
        toolbar_refresh = '<li style="%s">%s</li>' % (toolbar_refresh_style,refresh_list.xml())
        toolbar_input_search = '<li>%s %s</li>' % (input_search, do_search.xml())
        toolbar = '<ul>%s %s %s</ul>' % (toolbar_register,toolbar_refresh,toolbar_input_search)    
        list = '<div class="toolbar" style="height: 40px; width: 500px;">%s</div>' % toolbar        
            
        if last_users: 
            
            #create the header column   
            
            checkbox_all = '<input type="checkbox" id="checkboxall" />'
            caption_column1 = checkbox_all
            caption_column2 = T('Avatar')
            caption_column3 = T('Last name')
            caption_column4 = T('First name')
            caption_column5 = T('Email') 
            caption_column6 = T('Status')
            caption_column7 = T('Actions') 
            caption_column8 = T('Created')                
            row_column1 = '<div class="column1">%s</div>' % caption_column1
            row_column2 = '<div class="column2">%s</div>' % caption_column2
            row_column3 = '<div class="column3">%s</div>' % caption_column3
            row_column4 = '<div class="column4">%s</div>' % caption_column4
            row_column5 = '<div class="column5">%s</div>' % caption_column5
            row_column6 = '<div class="column6">%s</div>' % caption_column6
            row_column7 = '<div class="column7">%s</div>' % caption_column7
            row_column8 = '<div class="column8">%s</div>' % caption_column8        
            row_clear = '<div style="clear: both;"></div>'            
            
            row_user_xml = '<div class="row-user-headers"> %s %s %s %s %s %s %s %s %s </div>' \
                            % (row_column1,row_column2,row_column3,row_column4,\
                               row_column5,row_column6,row_column7,row_column8,row_clear)
            list += row_user_xml
            
            #titles are hints
            title_edit_firstname = T('Click to change the first name of this user')
            title_edit_lastname = T('Click to change the last name of this user')
            title_edit_email = T('Click to change the email of this user')
            title_delete = T('Click to delete this user')
            title_activate = T('Click to activate this user, this will delete the disabled, blocked and pending status of the current user')
            title_disable = T('Click to disable this user')
            title_changepass = T('Click to change pass')
            title_setasadmin = T('Click to set this user as an admin. In AppEngine make an admin in your Appspot account')
            title_block = T('Click to block this user')
            
            #id group admin
            id_group_admin = auth.id_group(self.i2p.config.group_admin)
            
            for user in last_users:                        
                            
                title_avatar = T('User ID: %s'%user.id)            
                if user.registration_key == 'pending':
                    caption_status = '<span style="color: orange;">' + str(T('Pending')) + '</span>'           
                elif user.registration_key == 'disabled':
                    caption_status = '<span style="color: orange;">' + str(T('Disabled'))+ '</span>'
                elif user.registration_key == 'blocked':
                    caption_status =  '<span style="color: orange;">' + str(T('Blocked')) + '</span>'  
                else:
                    caption_status = '<span style="color: green;">' + str(T('Active')) + '</span>'  
                                
                if auth.has_membership(id_group_admin, user.id, self.i2p.config.group_admin):  
                    caption_status += ', <span style="color: red;">' + str(T('Admin'))+ '</span>'  
                    
                checkbox_user = '<input type="checkbox" id="checkbox-%s" />'%user.id                
                icon_avatar = IMG(_src=URL(request.application,'static','images/avatar.png'), \
                                  _alt="avatar", _width="24px", _height="24px", \
                                  _title="%s"%title_avatar)                          
                link_edit_firstname = A(user.first_name, _href='javascript: void(0);', \
                                        _onclick="UserFirstName(%s);"%(user.id), \
                                        _title="%s"%title_edit_firstname)
                link_edit_lastname = A(user.last_name, _href='javascript: void(0);', \
                                       _onclick="UserLastName(%s);"%(user.id), \
                                       _title="%s"%title_edit_lastname)
                link_edit_email = A(user.email , _href='javascript: void(0);', \
                                    _onclick="UserEmail(%s);"%(user.id), \
                                    _title="%s"%title_edit_email)    
                
                icon_remove = IMG(_src=URL(request.application,'static','images/remove.png'), \
                                  _alt="remove")
                link_delete = A(icon_remove , _href='javascript: void(0);', \
                                _onclick="UserDelete(%s);"%(user.id), \
                                _title="%s"%title_delete)            
                icon_activate = IMG(_src=URL(request.application,'static','images/activate.png'), \
                                    _alt="activate")
                link_activate = A(icon_activate , _href='javascript: void(0);', \
                                  _onclick="UserActivate(%s);"%(user.id), \
                                  _title="%s"%title_activate)        
                icon_disable = IMG(_src=URL(request.application,'static','images/disable.png'), \
                                   _alt="disable")    
                link_desactivate = A(icon_disable , _href='javascript: void(0);', \
                                     _onclick="UserDisable(%s);"%(user.id), \
                                     _title="%s"%title_disable)          
                icon_change = IMG(_src=URL(request.application,'static','images/pass.gif'), \
                                  _alt="change pass")  
                link_change = A(icon_change, _href='javascript: void(0);', \
                                _onclick="UserPassword(%s);"%(user.id), \
                                _title="%s"%title_changepass)
                icon_setadmin = IMG(_src=URL(request.application,'static','images/setadmin.png'), \
                                    _alt="set admin")            
                link_setadmin = A(icon_setadmin , _href='javascript: void(0);', \
                                  _onclick="UserSetAdmin(%s);"%(user.id), \
                                  _title="%s"%title_setasadmin)
                link_block = A(icon_disable , _href='javascript: void(0);', \
                               _onclick="UserBlock(%s);"%(user.id), \
                               _title="%s"%title_block)
                link_actions = link_delete.xml() + ' ' +  link_activate.xml() + ' ' + \
                                link_desactivate.xml() + ' ' + link_change.xml() + ' ' + \
                                link_setadmin.xml() + ' ' + link_block.xml()
                created_on = user.created_on.strftime("%Y-%m-%d:%I:%M:%p")
                
                row_column1 = '<div class="column1">%s</div>' % checkbox_user
                row_column2 = '<div class="column2">%s</div>' % icon_avatar.xml() 
                row_column3 = '<div class="column3">%s</div>' % link_edit_lastname.xml()
                row_column4 = '<div class="column4">%s</div>' % link_edit_firstname.xml()
                row_column5 = '<div class="column5">%s</div>' % link_edit_email.xml()
                row_column6 = '<div class="column6">%s</div>' % caption_status
                row_column7 = '<div class="column7">%s</div>' % link_actions
                row_column8 = '<div class="column8">%s</div>' % created_on           
                row_clear = '<div style="clear: both;"></div>'            
                
                row_user_xml = '<div class="row-user" id="row-%s"> %s %s %s %s %s %s %s %s %s</div>' \
                                % (user.id,row_column1,row_column2,row_column3,row_column4,\
                                   row_column5,row_column6,row_column7,row_column8,row_clear)
                list += row_user_xml
                        
            if count_users>max_users:
                total_pages = count_users // max_users
                if (count_users % max_users)>0:
                    total_pages += 1
                
                first_page = int(math.ceil(currentpage / max_display_pages)) * max_display_pages
                if first_page<1:
                    first_page=1                
                    if total_pages < max_display_pages:
                        last_page = total_pages
                    else:            
                        last_page=max_display_pages
                else:
                    last_page=first_page + max_display_pages
                
                backward = A(T("Prior"), _href='javascript: void(0);', \
                             _onclick="UsersList(%s,'%s');"%(currentpage-1,search_text))           
                forward = A(T("Next"), _href='javascript: void(0);', \
                            _onclick="UsersList(%s,'%s');"%(currentpage+1,search_text))
                
                listpages=""    
                if currentpage>1:
                    listpages += "<li>%s</li>" % backward.xml()                             
                
                for page in range(first_page, last_page+1):                
                    page_a = A(unicode(page), _href='javascript: void(0);', \
                               _onclick="UsersList(%s,'%s');"%(page,search_text))
                    
                    if page<=total_pages:                       
                        if page==currentpage:
                            class_current = ' class="current"'
                        else:
                            class_current = '' 
                        listpages += "<li%s>%s</li>" % (class_current, page_a.xml())                                        
                    
                if total_pages>currentpage:
                    listpages += "<li>%s</li>" % forward.xml()
                
                if listpages!="":                      
                    list+='<div class="pages"><ul>%s</ul></div>' % listpages                  
                   
            page_content=list
        else:
            page_content=list + "%s"%T("No users") 
        
        html_content = '<h2>%s</h2>'%T("Users")
        html_content += "%s"%page_content
        info={}          
        info['html']=sanitate_string(html_content)        
        return sj.dumps(info)   
    
    
    
    
    def delete(self, id):  
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        session = self.i2p.environment.session
        auth = self.i2p.environment.auth        
            
        users = db(db.auth_user.id == id).select()
        if users:
            user = users[0]
            if user.email!=self.i2p.config.email or request.env.web2py_runtime_gae:
                if not request.env.web2py_runtime_gae:  
                    if user.email==auth.user.email:                        
                        return json_response(message=T("You cannot delete yourself!"),\
                                         alert=2,value="") 
                id_user = user.id
                db(db.auth_group.role=='user_%s'%id_user).delete()
                db(db.auth_membership.user_id==id_user).delete()  
                db(db.auth_user.id == id_user).delete()               
                return json_response(message=T("User deleted"),\
                                     alert=0,value="")            
                           
            else:            
                return json_response(message=T("You cannot delete default user!"),\
                                     alert=2,value="")
        else:
            return json_response(message=T("The user doesn't exist!"),\
                                 alert=2,value="")
        
        
        
    def disable(self, id):  
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        session = self.i2p.environment.session
        auth = self.i2p.environment.auth     
         
        users = db(db.auth_user.id == id).select()
        if users:
            user = users[0]
            if not request.env.web2py_runtime_gae:  
                if user.email==auth.user.email:                        
                    return json_response(message=T("You cannot disable yourself!"),\
                                 alert=2,value="") 
                                    
            user.update_record(registration_key = 'disabled')            
            return json_response(message=T("User disabled"),\
                                 alert=0,value="")           
                  
        else:        
            return json_response(message=T("The user doesn't exist!"),\
                                 alert=2,value="")   
        
        
        
        
    def activate(self, id): 
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        session = self.i2p.environment.session
        auth = self.i2p.environment.auth    
           
        users = db(db.auth_user.id == id).select()
        if users:
            user = users[0]
            if user.email!=self.i2p.config.email or request.env.web2py_runtime_gae: 
                if not request.env.web2py_runtime_gae:  
                    if user.email==auth.user.email:                        
                        return json_response(message=T("You cannot activate yourself!"), \
                                         alert=2,value="")                                                   
                
                user.update_record(registration_key = '')                
                return json_response(message= T("User activated"),\
                                     alert=0,value="")             
                
            else:            
                return json_response(message=T("You cannot activate default user!"),\
                                     alert=2,value="")           
        else:
            return json_response(message=T("The user doesn't exist!"),\
                                 alert=2,value="")
        
        
        
    
    def setadmin(self, id):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        session = self.i2p.environment.session
        auth = self.i2p.environment.auth 
        
        users = db(db.auth_user.id == id).select()
        if users:
            user = users[0]
            if user.email!=self.i2p.config.email or request.env.web2py_runtime_gae:       
                if not request.env.web2py_runtime_gae:  
                    if user.email==auth.user.email:                        
                        return json_response(message=T("You cannot set as admin yourself!"),\
                                         alert=2,value="")
                                        
                id_group_admin = auth.id_group(self.i2p.config.group_admin)
                if auth.has_membership(id_group_admin, user.id, self.i2p.config.group_admin):
                    auth.del_membership(id_group_admin, user.id)
                    return json_response(message=T("User has been removed from admin list") ,\
                                         alert=0,value="")
                else:
                    auth.add_membership(id_group_admin,  user.id)
                    return json_response(message=T("User has been added to admin list"),\
                                         alert=0,value="")               
                          
            else:            
                return json_response(message=T("You cannot edit default user!"),\
                                     alert=2,value="")  
        else:
            return json_response(message=T("The user doesn't exist!"),\
                                 alert=2,value="") 
        
        
        
    def save_firstname(self, id, value):  
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        session = self.i2p.environment.session
        auth = self.i2p.environment.auth
        
        value =  value.strip()  
        users = db(db.auth_user.id == id).select()
        if users:
            user = users[0]
            if user.email!=self.i2p.config.email or request.env.web2py_runtime_gae:
                user.update_record(first_name = value)            
                return json_response(message=T('Firstname updated'),\
                                     alert=0,value="")
            else:            
                return json_response(message=T("You cannot edit default user!"),\
                                     alert=2,value="")
        else:
            return json_response(message=T("The user doesn't exist!"),\
                                 alert=2,value="")
        
        
    
    
    def save_lastname(self, id, value):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        session = self.i2p.environment.session
        auth = self.i2p.environment.auth
        
        
        value =  value.strip()    
        users = db(db.auth_user.id == id).select()
        if users:
            user = users[0]
            if user.email!=self.i2p.config.email or request.env.web2py_runtime_gae:
                user.update_record(last_name = value)            
                return json_response(message=T('Lastname updated'),\
                                     alert=0,value="")
            else:
                return json_response(message=T("You cannot edit default user!"),\
                                     alert=2,value="")
        else:
            return json_response(message=T("The user doesn't exist!"),\
                                 alert=2,value="")
        
        
    #need to check if IS IN DB    
    def save_email(self, id, value):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        session = self.i2p.environment.session
        auth = self.i2p.environment.auth
           
        value =  value.strip()  
        notvalid = (IS_EMAIL()(value))[1]
        if notvalid:
            return json_response(message=T("The email is not valid"),\
                                 alert=2,value="")
             
        users = db(db.auth_user.id == id).select()
        if users:
            user = users[0]
            if user.email!=self.i2p.config.email or request.env.web2py_runtime_gae:
                user.update_record(email = value)            
                return json_response(message=T('Email updated'),\
                                     alert=0,value="")
            else:
                return json_response(message=T("You cannot edit default user!"),\
                                     alert=2,value="")
        else:
            return json_response(message=T("The user doesn't exist!"),\
                                 alert=2,value="")
        
        
        
    def get_email(self, id):    
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        
        users = db(db.auth_user.id == id).select()
        if users:
            user = users[0]
            value = user.email        
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message=T("The user doesn't exist!"),\
                                 alert=2,value="")
        
        
        
    def get_firstname(self, id):
        
        db = self.i2p.db
        T = self.i2p.environment.T
             
        users = db(db.auth_user.id == id).select()
        if users:
            user = users[0]
            value = user.first_name
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message=T("The user doesn't exist!"),\
                                 alert=2,value="")
        
        
        
    def get_lastname(self, id):  
        
        db = self.i2p.db
        T = self.i2p.environment.T
         
        users = db(db.auth_user.id == id).select()
        if users:
            user = users[0]
            value = user.last_name
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message=T("The user doesn't exist!"),\
                                 alert=2,value="")
        
        
        
        
    def block(self, id):  
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        session = self.i2p.environment.session
        auth = self.i2p.environment.auth
          
        users = db(db.auth_user.id == id).select()
        if users:
            user = users[0]
            if not request.env.web2py_runtime_gae:  
                if user.email==auth.user.email:                        
                    return json_response(message= T("You cannot block yourself!"),\
                                     alert=2,value="")            
            user.update_record(registration_key = 'blocked')            
            return json_response(message=T("User blocked"),\
                                 alert=0,value="")           
                
        else:        
            return json_response(message=T("The user doesn't exist!"),\
                                 alert=2,value="")  



    def change_password(self, id, value):  
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        session = self.i2p.environment.session
        auth = self.i2p.environment.auth
          
        value =  value.strip()  
        notvalid = (IS_LENGTH(minsize=6)(value))[1]
        if notvalid:
            return json_response(message=T("The password is not valid, the minsize of a password is 6 character"),\
                                 alert=2,value="")
        
        users = db(db.auth_user.id == id).select()
        if users:
            user = users[0]
            if user.email!=self.i2p.config.email or request.env.web2py_runtime_gae:   
                if not request.env.web2py_runtime_gae:  
                    if user.email==auth.user.email:                        
                        return json_response(message=T("You cannot change your password in this panel, use your profile"),\
                                         alert=2,value="")
                         
                my_crypt = CRYPT(key=auth.settings.hmac_key)
                crypt_pass = my_crypt(value)[0] 
                user.update_record(password = crypt_pass)                               
                return json_response(message= T("User password changed"),\
                                     alert=0,value="")               
                              
            else:            
                return json_response(message=T("You cannot change passwor of the default user!"),\
                                     alert=2,value="")           
        else:
            return json_response(message=T("The user doesn't exist!"),\
                                 alert=2,value="")



    #this only return a random generated password,
    #the password are hashed in db.
    def get_password(self, id):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        def random_password():
            import string
            import random
            password = ''
            specials=r'!#$*'
            for i in range(0,3):
                password += random.choice(string.lowercase)
                password += random.choice(string.uppercase)
                password += random.choice(string.digits)
                password += random.choice(specials)
            return ''.join(random.sample(password,len(password)))
             
        users = db(db.auth_user.id == id).select()
        if users:
            user = users[0]
            value = random_password()         
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message=T("The user doesn't exist!"),\
                                 alert=2,value="")

