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

#is user an admin
def is_user_an_admin():
    
    if request.env.web2py_runtime_gae:
        from google.appengine.api import users
        if users.is_current_user_admin():
            return True        
    else:
        if 'auth' in globals():
            if auth.is_logged_in():   
                is_admin = auth.has_membership(auth.id_group(i2p.config.group_admin))
                if is_admin:
                    return True    
    return False 

#added support to gae admin users
def check_credentials_is_admin():    
    is_an_admin = is_user_an_admin()
    if not is_an_admin:
        if request.env.web2py_runtime_gae:
            from google.appengine.api import users
            login_html = '<a href="%s">%s</a>.' \
                % (users.create_login_url(request.env.path_info), T('Sign in with your google account'))
            raise HTTP(200, '<html><body>%s</body></html>' % login_html)
        else:
            next = auth.settings.on_failed_authorization
            redirect(next)
            
    return is_an_admin
           
                
#The user is logged in?
def is_user_logged_in():
    logged_in=False
    if 'auth' in globals():
        if auth.is_logged_in():
            logged_in=True 
    
    return logged_in   


def pretty_exceptions(title="not found", message="this is the problem"):    
    
    img_warning = IMG(_src=URL(request.application,'static','images/warning.png'), _alt="Warning",_style="float: left; padding: 5px;")
    link_index = A(T('Back to the index page'), _href=URL(request.application,'default','index'))
    html =  '''
    <!DOCTYPE html>
    <html lang="en">
    <head>    
    <meta charset="utf-8">          
    <title>%(title)s</title>
    <style type="text/css">
    body {
        margin: 0;
        padding: 0;
        background: #fff;     
        font-family: Arial,Helvetica,sans-serif;     
        color: #444;
    }
    #wrapper {
        margin: 0 auto;
        padding: 0;
    }
    #page {
        width: 500px;
        margin: 0 auto;
        padding: 40px;        
    }
    #warning {       
        -webkit-border-radius: 5px;
        -moz-border-radius: 5px;
        border-radius: 5px;    
        width: 350px
        padding: 20px;        
        background-color: #fff;
        border: 1px solid #d0cfc2;            
        }
    .title {       
        font-size: 20px; 
        font-weight: bold;                   
        } 
    .content {        
        padding: 20px;           
        }
    .description {        
        font-size: 16px;             
        }     
    </style>
    </head>       
    <body>
    <div id="wrapper">
    <div id="page">
    <div id="warning"> 
        %(image)s 
        <div class="content"> 
        <div class="title"> %(title)s </div> 
        <div class="description">%(message)s <p>%(index)s</p> </div> 
        <div style="clear: both; float: none;"></div>
        </div>
    </div>
    </div>
    </div>
    </body>
    </html>    
    ''' % {'title': title, 'image': img_warning.xml(), 'message':message,'index':link_index.xml()}
    
    return html    
