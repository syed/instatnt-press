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


ADMIN_LINKS_LIST_PER_PAGE = 5
ADMIN_MAX_LIST_PAGES = 10

class Links(object): 
    
    def __init__(self, i2p):
        
        self.i2p = i2p        
               
        
    def define_tables(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        db.define_table('links',                                  
            Field('id', 'id'),
            Field('name', 'string', length=512, requires=(IS_SLUG())),     
            Field('title', 'string', length=512, required=True),
            Field('url', 'text', default="", requires=(IS_URL())),
            Field('description', 'text', default=""), 
            Field('created_on', 'datetime', default=datetime.datetime.today()),                                                                                                                        
            migrate=self.i2p.config.is_first_time)
        
        
class admLinks(object): 
    
    def __init__(self, i2p):
        
        self.i2p = i2p  
                
    #admin view    
    def list(self, currentpage=1, search_text=""):        
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        if not isinstance(search_text, (unicode, str) ): 
            search_text = ""            
            
        max_links=ADMIN_LINKS_LIST_PER_PAGE
        max_display_pages=ADMIN_MAX_LIST_PAGES
        
        limit_inf = (max_links * currentpage) - max_links
        limit_sup = limit_inf + max_links 
        
        count_links = db(db.links.id>0).count()
        last_links = db(db.links.id>0).select(db.links.ALL,\
                                              orderby=~db.links.created_on,\
                                              limitby=(limit_inf, limit_sup))
        
        add_links = A(T("Add"), _href='javascript: void(0);', \
                      _onclick="LinkAdd();",\
                      _title="%s"%T('Add a new link'))  
        icon_link_url = URL(request.application,'static','images/toolbar_add.png')    
        toolbar_new_link_style = 'padding-left: 20px; background-image: url(%s); background-repeat: no-repeat;' \
                                % icon_link_url
        
        refresh_list = A(T("Refresh"), _href='javascript: void(0);', \
                         _onclick="LinkList(1);", \
                         _title="%s"%T('Reload the list'))
        icon_refresh_url = URL(request.application,'static','images/toolbar_refresh.png')    
        toolbar_refresh_style = 'padding-left: 20px; background-image: url(%s); background-repeat: no-repeat;' \
                                % icon_refresh_url
            
        toolbar_new_link = '<li style="%s">%s</li>' % (toolbar_new_link_style,add_links.xml())
        toolbar_refresh = '<li style="%s">%s</li>' % (toolbar_refresh_style,refresh_list.xml())
        toolbar = '<ul>%s %s</ul>' % (toolbar_new_link,toolbar_refresh)    
        list = '<div class="toolbar" style="height: 30px; width: 300px;">%s</div>' % toolbar        
        
        if last_links:  
            
            #create the header column   
            caption_column1 = T('Title')
            caption_column2 = T('Url')
            caption_column3 = T('Description')
            caption_column4 = T('Action')
            
            row_column1 = '<div class="column1">%s</div>' % caption_column1
            row_column2 = '<div class="column2">%s</div>' % caption_column2
            row_column3 = '<div class="column3">%s</div>' % caption_column3
            row_column4 = '<div class="column4">%s</div>' % caption_column4                        
            row_clear = '<div style="clear: both;"></div>'            
            
            row_links_xml = '<div class="row-links-headers"> %s %s %s %s %s </div>' \
                            % (row_column1,row_column2,row_column3,row_column4,row_clear)
            list += row_links_xml        
            
            #titles are hints
            title_change_title = T('Click to change title')
            title_change_url = T('Click to change url site')
            title_change_description = T('Click to change description')
            title_remove = T('Click to delete this link')
            
            icon_remove = IMG(_src=URL(request.application,'static','images/remove.png'), \
                              _alt="remove")
               
            for link in last_links:                        
                link_id = A(link.id, _href='javascript: void(0);', \
                            _onclick="LinkGoTo(%s);"%(link.id))
                link_title = A(link.title[:50], _href='javascript: void(0);', \
                               _onclick="LinkChangeTitle(%s);"%(link.id), \
                               _title="%s"%title_change_title)            
                if link.url!="":
                    caption_url = link.url[:40] + "..."
                else:
                    caption_url = T('Empty')            
                link_url = A(caption_url, _href='javascript: void(0);', \
                             _onclick="LinkChangeUrl(%s);"%(link.id), \
                             _title="%s"%title_change_url)
                
                if link.description!="":                
                    caption_description=link.description[:50]
                else:
                    caption_description=T("No description")                
                link_description = A(caption_description, _href='javascript: void(0);', \
                                     _onclick="LinkChangeDescription(%s);"%(link.id), \
                                     _title="%s"%title_change_description)                        
                link_delete = A(icon_remove, _href='javascript: void(0);', \
                                _onclick="LinkDelete(%s);"%(link.id), \
                                _title="%s"%title_remove)
                                        
                row_column1 = '<div class="column1">%s</div>' % link_title.xml()
                row_column2 = '<div class="column2">%s</div>' % link_url.xml()
                row_column3 = '<div class="column3">%s</div>' % link_description.xml()
                row_column4 = '<div class="column4">%s</div>' % link_delete.xml()                       
                row_clear = '<div style="clear: both;"></div>'            
                
                row_link_xml = '<div class="row-links" id="row-%s"> %s %s %s %s %s </div>' \
                                % (link.id,row_column1,row_column2,row_column3,row_column4,row_clear)
                list += row_link_xml            
            
            if count_links>max_links:
                total_pages = count_links // max_links
                if (count_links % max_links)>0:
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
                             _onclick="LinkList(%s);"%(currentpage-1))           
                forward = A(T("Next"), _href='javascript: void(0);', \
                            _onclick="LinkList(%s);"%(currentpage+1))
                
                
                listpages=""    
                if currentpage>1:
                    listpages += "<li>%s</li>" % backward.xml()                             
                
                for page in range(first_page, last_page+1):                
                    page_a = A(unicode(page), _href='javascript: void(0);', \
                               _onclick="LinkList(%s);"%(page))
                    
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
            page_content=list + "%s"%T("No links")
        
        html_content = '<h2>%s</h2>'%T("Links")
        html_content += "%s"%page_content
        info={}          
        info['html']=sanitate_string(html_content)        
        return sj.dumps(info)  
    
    
    
    
    def add(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        
        default_url = 'http://www.mysiteurl.com'          
        default_title = sanitate_string("%s"%T('No Title'))
        default_name = (IS_SLUG()("%s"%T('No Title')))[0]
        idlink = db.links.insert(title = default_title, 
                                 name = default_name, 
                                 url=default_url)    
        if idlink>0:  
            return json_response(message= T("Link added"),\
                                 alert=0,value=idlink)      
        else:
            return json_response(message=T("The link doesn't exist!"),\
                                 alert=2,value="")  

        
    
     
    def change_title(self, id, value): 
        
        db = self.i2p.db
        T = self.i2p.environment.T
                   
        links = db(db.links.id == id).select()
        if links:
            link = links[0]             
            name = (IS_SLUG()(value))[0] #change also the name
            link.update_record(title = value, 
                               name = name)        
            return json_response(message= T("Title changed"),\
                                 alert=0,value="")        
        else:
            return json_response(message=T("The link doesn't exist!"),\
                                 alert=2,value="")   
        


     
    def get_title(self, id):  
        
        db = self.i2p.db
        T = self.i2p.environment.T
          
        links = db(db.links.id == id).select()
        if links:
            link = links[0]
            value = link.title        
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message=T("The link doesn't exist!"),\
                                 alert=2,\
                                 value="")
        
        
        
    
    def change_url(self, id, value): 
        
        db = self.i2p.db
        T = self.i2p.environment.T
            
        (url, notvalid) = (IS_URL()(value))
        if notvalid:
            return json_response(message=T("The url-link is not valid use: http://www.mysite.com"),\
                                 alert=2,value="")       
               
        links = db(db.links.id == id).select()
        if links:
            link = links[0]             
            link.update_record(url = url)        
            return json_response(message=T("Url changed"),\
                                 alert=0,value="")    
        else:
            return json_response(message=T("The link doesn't exist!"),\
                                 alert=2,value="")      



    
    def get_url(self, id): 
        
        db = self.i2p.db
        T = self.i2p.environment.T
           
        links = db(db.links.id == id).select()
        if links:
            link = links[0]
            value = link.url        
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message=T("The link doesn't exist!"),\
                                 alert=2,\
                                 value="")
        
        
        
       
    def change_description(self, id, value): 
        
        db = self.i2p.db
        T = self.i2p.environment.T
                   
        links = db(db.links.id == id).select()
        if links:
            link = links[0]             
            link.update_record(description = value)        
            return json_response(message=T("Description changed"),\
                                 alert=0,value="")    
        else:
            return json_response(message=T("The link doesn't exist!"),\
                                 alert=2,value="") 
        
        
        
      
    def get_description(self, id): 
        
        db = self.i2p.db
        T = self.i2p.environment.T
           
        links = db(db.links.id == id).select()
        if links:
            link = links[0]
            value = link.description        
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message=T("The link doesn't exist!"),\
                                 alert=2,value="")
        
    
    
    
    def delete(self, id):  
        
        db = self.i2p.db
        T = self.i2p.environment.T
              
        links = db(db.links.id == id).select()
        if links:
            link = links[0]
            idlink = link.id
            db(db.links.id == idlink).delete()        
            return json_response(message= T('Link deleted!'),\
                                 alert=0,value="")
        else:
            return json_response(message=T("The link doesn't exist!"),\
                                 alert=2,value="")

    


