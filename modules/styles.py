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
import os

from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *
from gluon.sql import *
import gluon.contrib.simplejson as sj

#local
from utils import *


ADMIN_STYLE_LIST_PER_PAGE = 5
ADMIN_MAX_LIST_PAGES = 10

class Styles(object): 
    
    def __init__(self, i2p):
        
        self.i2p = i2p        
               
        
        
    def define_tables(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        db.define_table('style',                                  
            Field('id', 'id'),
            Field('name', 'string', length=512, requires=(IS_SLUG())),     
            Field('title', 'string', length=512, required=True),
            Field('css', 'text', default=""),
            Field('layout', 'string', length=512, default="default"),
            Field('author', 'text', default=""),
            Field('link', 'text', default="", requires=(IS_URL())),
            Field('description', 'text', default=""), 
            Field('created_on', 'datetime', default=datetime.datetime.today()),                                                                                                                        
            migrate=self.i2p.config.is_first_time)



class admStyles(object): 
    
    def __init__(self, i2p):
        
        self.i2p = i2p     
                        
                        
    #admin view    
    def list(self, currentpage=1, search_text=""):        
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        if not isinstance(search_text, (unicode, str) ): 
            search_text = ""
                                    
        max_styles=ADMIN_STYLE_LIST_PER_PAGE
        max_display_pages=ADMIN_MAX_LIST_PAGES
        
        limit_inf = (max_styles * currentpage) - max_styles
        limit_sup = limit_inf + max_styles 
        
        count_style = db(db.style.id>0).count()
        last_style = db(db.style.id>0).select(db.style.ALL,\
                                              orderby=~db.style.created_on,\
                                              limitby=(limit_inf, limit_sup))
    
        add_style = A(T("Add"), _href='javascript: void(0);', \
                      _onclick="StyleAdd();",\
                      _title="%s"%T('Create a new style'))  
        icon_add_url = URL(request.application,'static','images/toolbar_add.png')    
        toolbar_add_style_style = 'padding-left: 20px; background-image: url(%s); background-repeat: no-repeat;' \
                                     % icon_add_url
        
        refresh_list = A(T("Refresh"), _href='javascript: void(0);', \
                         _onclick="StyleList(1);", \
                         _title="%s"%T('Reload the list'))
        icon_refresh_url = URL(request.application,'static','images/toolbar_refresh.png')    
        toolbar_refresh_style = 'padding-left: 20px; background-image: url(%s); background-repeat: no-repeat;' \
                                % icon_refresh_url
            
        toolbar_add_style = '<li style="%s">%s</li>' % (toolbar_add_style_style,add_style.xml())
        toolbar_refresh = '<li style="%s">%s</li>' % (toolbar_refresh_style,refresh_list.xml())
        toolbar = '<ul>%s %s</ul>' % (toolbar_add_style,toolbar_refresh)    
        list = '<div class="toolbar" style="height: 30px; width: 300px;">%s</div>' % toolbar        
        
        if last_style:  
            
            #create the header column   
            caption_column1 = T('Title')
            caption_column2 = T('Css')
            caption_column3 = T('Style')
            caption_column4 = T('Author')
            caption_column5 = T('Action')  
            caption_column6 = T('Created')       
            
            row_column1 = '<div class="column1">%s</div>' % caption_column1
            row_column2 = '<div class="column2">%s</div>' % caption_column2
            row_column3 = '<div class="column3">%s</div>' % caption_column3
            row_column4 = '<div class="column4">%s</div>' % caption_column4
            row_column5 = '<div class="column5">%s</div>' % caption_column5
            row_column6 = '<div class="column6">%s</div>' % caption_column6                
            row_clear = '<div style="clear: both;"></div>'            
            
            row_style_xml = '<div class="row-style-headers"> %s %s %s %s %s %s %s </div>' \
                            % (row_column1,row_column2,row_column3,row_column4,\
                               row_column5,row_column6,row_clear)
            list += row_style_xml        
            
            #titles are hints
            title_change_title = T('Click to change title')
            title_change_css = T('Click to change css')
            title_change_layout = T('Click to change style-layout from availables styles in the site')   
            title_delete = T('Click to delete')
            title_apply = T('Click to apply this style')
            icon_remove = IMG(_src=URL(request.application,'static','images/remove.png'), \
                              _alt="remove")
            icon_apply = IMG(_src=URL(request.application,'static','images/apply.png'), \
                             _alt="apply")
            icon_edit = IMG(_src=URL(request.application,'static','images/edit.png'), \
                            _alt="edit")
                    
            for style in last_style:                        
                link_id = A(style.id, _href='javascript: void(0);', \
                            _onclick="StyleGoTo(%s);"%(style.id))
                
                if style.title!="":
                    style_title = style.title[:50]
                else:
                    style_title = T("No title")
                
                link_title = A(style_title, _href='javascript: void(0);', \
                               _onclick="StyleChangeTitle(%s);"%(style.id),\
                               _title="%s"%title_change_title)            
                link_css = A(icon_edit, _href='javascript: void(0);', \
                             _onclick="StyleChangeCss(%s);"%(style.id),\
                             _title="%s"%title_change_css)
                link_layout = A(style.layout, _href='javascript: void(0);', \
                                _onclick="StyleShowAvailables(%s);"%(style.id),\
                                _title="%s"%title_change_layout)
                
                if style.author!="":
                    caption_author = style.author[:38] + "..."
                else:
                    caption_author = T('Edit')         
                
                link_author = A(caption_author, _href='javascript: void(0);', \
                                _onclick="StyleChangeAuthor(%s);"%(style.id))            
                link_delete = A(icon_remove, _href='javascript: void(0);', \
                                _onclick="StyleDelete(%s);"%(style.id),_title="%s"%title_delete)            
                link_apply = A(icon_apply, _href='javascript: void(0);', \
                               _onclick="StyleApply(%s);"%(style.id),_title="%s"%title_apply)            
                on_date = style.created_on.strftime("%Y-%m-%d:%I:%M:%p")
                                        
                row_column1 = '<div class="column1">%s</div>' % link_title.xml()
                row_column2 = '<div class="column2">%s</div>' % link_css.xml()
                row_column3 = '<div class="column3">%s</div>' % link_layout.xml()
                row_column4 = '<div class="column4">%s</div>' % link_author.xml()
                row_column5 = '<div class="column5">%s %s</div>' % (link_delete.xml(), link_apply.xml()) 
                row_column6 = '<div class="column6">%s</div>' % on_date          
                row_clear = '<div style="clear: both;"></div>'            
                
                row_style_xml = '<div class="row-style" id="row-%s"> %s %s %s %s %s %s %s </div>' \
                % (style.id,row_column1,row_column2,row_column3,row_column4,\
                   row_column5,row_column6,row_clear)
                list += row_style_xml            
            
            if count_style>max_styles:
                total_pages = count_style // max_styles
                if (count_style % max_styles)>0:
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
                             _onclick="StyleList(%s);"%(currentpage-1))           
                forward = A(T("Next"), _href='javascript: void(0);', \
                            _onclick="StyleList(%s);"%(currentpage+1))
                
                
                listpages=""    
                if currentpage>1:
                    listpages += "<li>%s</li>" % backward.xml()                             
                
                for page in range(first_page, last_page+1):                
                    page_a = A(unicode(page), _href='javascript: void(0);', \
                               _onclick="StyleList(%s);"%(page))
                    
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
            page_content=list + "%s"%T("No styles")
        
        html_content = '<h2>%s</h2>'%T("Styles")
        html_content += "%s"%page_content
        info={}          
        info['html']=sanitate_string(html_content)        
        return sj.dumps(info)  
    
    
    
    
    def add(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
                 
        default_title = sanitate_string("%s"%T('No Title'))
        default_name = (IS_SLUG()("%s"%T('No Title')))[0]
        default_css = self.i2p.siteinfo._get_default_style()
        idstyle = db.style.insert(title = default_title, 
                                  name = default_name, 
                                  css=default_css)    
        if idstyle>0:        
            return json_response(message= T("Style added"),\
                                 alert=0,value=idstyle)
        else:
            return json_response(message=T("The style doesn't exist!"),\
                                 alert=2,value="")  
        
        
       
    def change_title(self, id, value):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        alert = 2            
        styles = db(db.style.id == id).select()
        if styles:
            style = styles[0]  
            if style.name != 'default':               
                name = (IS_SLUG()(value))[0] #change also the name  
                if name!= 'default':      
                    style.update_record(title = value, name = name)        
                    return json_response(message=T("Title changed"),\
                                         alert=0,value="")
                else: 
                    return json_response(message= T("You cannot change 'default', please create another."),\
                                     alert=2,value="")  
            else:
                return json_response(message= T("You cannot change 'default', please create another."),\
                                     alert=2,value="")      
        else:
            return json_response(message=T("The style doesn't exist!"),\
                                 alert=2,value="")      
        
        
    
    def get_title(self, id): 
        
        db = self.i2p.db
        T = self.i2p.environment.T
            
        styles = db(db.style.id == id).select()
        if styles:
            style = styles[0]
            value = style.title        
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message=T("The style doesn't exist!"),\
                                 alert=2,value="")
 
       
    
    def change_css(self, id, value):
        
        db = self.i2p.db
        T = self.i2p.environment.T
            
        styles = db(db.style.id == id).select()
        if styles:
            style = styles[0]
            if style.name != 'default':                     
                style.update_record(css = value)            
                return json_response(message= T("Css changed"),\
                                     alert=0,value="")
            else:              
                return json_response(message= T("You cannot edit 'default' CSS, please create another."),\
                                     alert=2,value="")                  
        else:
            return json_response(message=T("The style doesn't exist!"),\
                                 alert=2,value="")       


    
    def get_css(self, id): 
                
        db = self.i2p.db
        T = self.i2p.environment.T
            
        styles = db(db.style.id == id).select()
        if styles:
            style = styles[0]
            value = style.css        
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message=T("The style doesn't exist!"),\
                                 alert=2,value="")
        
        
      
    def change_author(self, id, value):  
        
        db = self.i2p.db
        T = self.i2p.environment.T
          
        styles = db(db.style.id == id).select()
        if styles:
            style = styles[0]             
            style.update_record(author = value)        
            return json_response(message=T("Author changed"),\
                                 alert=0,value="")     
        else:
            return json_response(message=T("The style doesn't exist!"),\
                                 alert=2,value="") 
        
        
     
    def get_author(self, id):  
        
        db = self.i2p.db
        T = self.i2p.environment.T
           
        styles = db(db.style.id == id).select()
        if styles:
            style = styles[0]
            value = style.author
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message=T("The style doesn't exist!"),\
                                 alert=2,value="")
      

    
    def delete(self, id):
        
        db = self.i2p.db
        T = self.i2p.environment.T
                
        styles = db(db.style.id == id).select()
        if styles:
            style = styles[0]
            idstyle = style.id
            if style.name != 'default':
                db(db.style.id == idstyle).delete()            
                return json_response(message= T('Style deleted!'),\
                                     alert=0,value="")
            else:              
                return json_response(message= T('You cannot delete default style'),\
                                     alert=2,value="")            
        else:
            return json_response(message=T("The style doesn't exist!"),\
                                 alert=2,value="")


    
    def apply(self, id):
        
        db = self.i2p.db
        T = self.i2p.environment.T
                 
        styles = db(db.style.id == id).select()
        if styles:
            style = styles[0]
            style_css = style.css
            style_layout = style.layout
            siteinfo = db(db.siteinfo.id>0).select()
            if siteinfo:
                info = siteinfo[0]                     
                info.update_record(site_css = style_css,
                                   site_layout = style_layout)
                return json_response(message=T('The style has been apply! Reload the site to see the changes.'), \
                                     alert=0,value="")
            else:
                return json_response(message=T("The style doesn't exist!"),\
                                     alert=2,value="")                       
        else:
            return json_response(message=T("The style doesn't exist!"),\
                                 alert=2,value="")
            
            
    #get dir from view/styles and check if meet the requirement 
    #all dirs that contains needit files like style.css, footer.html, etc.
    #if you want to make new layout the best way is to copy from an exist folder to newone
    def _get_dir_styles(self):
            
                
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
                
               
        path_layout =os.path.join(request.folder,'views/styles/') #get the full path to layouts
        #need_files = ['style.css','footer.html','header.html','sidebar.html']
#        need_files = ['style.css','default/default/footer.html','default/default/header.html', 
#                      'default/default/sidebar.html','default/default/_css.html',
#                      'default/index/footer.html','default/index/header.html',
#                      'default/index/sidebar.html','default/index/_css.html',
#                      'default/search/footer.html','default/search/header.html',
#                      'default/search/sidebar.html','default/search/_css.html',
#                      'default/view/footer.html','default/view/header.html',
#                      'default/view/sidebar.html','default/view/_css.html' ]   

        need_files = ['style.css']     
        
        names = os.listdir(path_layout)
        dirs = []    
        for name in names:
            if os.path.isdir(os.path.join(path_layout, name)):
                problem=False
                for file in need_files:
                    file_required = os.path.join(path_layout, name, file)
                    if not os.path.exists(file_required):
                        problem=True
                if not problem:                     
                    dirs.append(name)
                    
        return dirs
                        
            
            
    def availables(self, id):   
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        xml_styles = ""
        lis_styles = ""
        caption_title = T('Styles availables')    
        styles = self._get_dir_styles() #get the list of styles in the folders view/styles
        if styles:
            for style in styles:
                link_2_style = A(str(T("Apply")) +" "+ style, _href='javascript: void(0);', \
                                    _onclick="StyleChangeStyle(%s,'%s');"%(id,style)) 
                li_styles = '<li> %s </li>' % link_2_style
                lis_styles += li_styles
            
            xml_styles = '<h2>%s</h2><div style="height: 200px; overflow-y: scroll; "><ul>%s</ul></div>' \
                            % (caption_title, lis_styles)
            message=""
            alert=0
        else:
            xml_styles = '<h2>%s</h2><ul>%s</ul>' % (caption_title, T("No styles"))
            message=T("Error No styles in directory!.")
            alert=1      
            
        
        return json_response(message,alert,value=xml_styles)
    
    
    
    def change_style(self, id, value):  
        
        db = self.i2p.db
        T = self.i2p.environment.T
          
        styles = db(db.style.id == id).select()
        if styles:
            style = styles[0]
            if style.name != 'default':                
                css = self.i2p.siteinfo._get_default_style(value)                          
                style.update_record(layout = value, css = css)        
                return json_response(message=T("Style changed"),\
                                     alert=0,value="")
            else:
                return json_response(message= T("You cannot change 'default' style, please add new style."),\
                                     alert=2,value="")                     
        else:
            return json_response(message=T("The style doesn't exist!"),\
                                 alert=2,value="") 

            
