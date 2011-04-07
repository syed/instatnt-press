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

ADMIN_MAX_LIST_PAGES = 10
ADMIN_CATS_LIST_PER_PAGE = 5


class Categories(object): 
    
    def __init__(self, i2p):
        
        self.i2p = i2p       
     
    
    def define_tables(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        db.define_table('categories',                                  
            Field('id', 'id'),
            Field('name', 'string', length=512, requires=(IS_SLUG())),     
            Field('title', 'string', length=512, required=True),         
            Field('description', 'text', default=""),                      
            Field('created_on', 'datetime', default=datetime.datetime.today()),                                                                                                          
            migrate=self.i2p.config.is_first_time)
        
        db.define_table('categorieslist',                                  
            Field('id', 'id'),
            Field('cat_id', 'integer', required=True),     
            Field('post_id', 'integer', required=True),                                                                                                                         
            migrate=self.i2p.config.is_first_time)
        
        db.categorieslist.cat_id.requires = IS_IN_DB(db, 'categories.id', 'categories.title')
        db.categorieslist.post_id.requires = IS_IN_DB(db, 'posts.id', 'posts.title')
        
        
        
    def get_list(self, page=1, limit=1000):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        (limit_inf, limit_sup) = get_query_limits(page, limit)    
        last_cats = db(db.categories.id>0).select(db.categories.ALL, \
                                                  orderby=db.categories.title, \
                                                  limitby=(limit_inf, limit_sup))    
        
        return last_cats
    

class admCategories(object): 
    
    def __init__(self, i2p):
        
        self.i2p = i2p  
    
        
      
    def list(self, currentpage=1, search_text=""):        
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        if not isinstance(search_text, (unicode, str) ): 
            search_text = ""
        
        max_categories=ADMIN_CATS_LIST_PER_PAGE
        max_display_pages=ADMIN_MAX_LIST_PAGES
        
        limit_inf = (max_categories * currentpage) - max_categories
        limit_sup = limit_inf + max_categories 
            
        count_categories = db(db.categories.id>0).count()
        last_categories = db(db.categories.id>0).select(db.categories.ALL, \
                                                        orderby=~db.categories.created_on, \
                                                        limitby=(limit_inf, limit_sup))
        
        new_cat = A(T("Add"), _href='javascript: void(0);', \
                    _onclick="CategoryAdd();", \
                    _title="%s"%T('Create a new category'))  
        icon_cat_url = URL(request.application,'static','images/toolbar_add.png')    
        toolbar_new_cat_style = 'padding-left: 20px; background-image: url(%s); background-repeat: no-repeat;' \
                                % icon_cat_url
        
        refresh_list = A(T("Refresh"), _href='javascript: void(0);', \
                         _onclick="CategoryList(1);", \
                         _title="%s"%T('Reload the list'))
        icon_refresh_url = URL(request.application,'static','images/toolbar_refresh.png')    
        toolbar_refresh_style = 'padding-left: 20px; background-image: url(%s); background-repeat: no-repeat;' \
                                % icon_refresh_url
            
        toolbar_new_cat = '<li style="%s">%s</li>' % (toolbar_new_cat_style,new_cat.xml())
        toolbar_refresh = '<li style="%s">%s</li>' % (toolbar_refresh_style,refresh_list.xml())
        toolbar = '<ul>%s %s</ul>' % (toolbar_new_cat,toolbar_refresh)    
        list = '<div class="toolbar" style="height: 30px; width: 300px;">%s</div>' % toolbar        
        
        if last_categories:        
            
            #create the header column   
            caption_column1 = T('Title')
            caption_column2 = T('Name')
            caption_column3 = T('Description')
            caption_column4 = T('Actions')        
            
            row_column1 = '<div class="column1">%s</div>' % caption_column1
            row_column2 = '<div class="column2">%s</div>' % caption_column2
            row_column3 = '<div class="column3">%s</div>' % caption_column3
            row_column4 = '<div class="column4">%s</div>' % caption_column4
                    
            row_clear = '<div style="clear: both;"></div>'            
            
            row_article_xml = '<div class="row-categories-headers"> %s %s %s %s %s </div>' \
                            % (row_column1,row_column2,row_column3,row_column4,row_clear)
            list += row_article_xml  
            
            #titles are hints
            title_change_title = T('Click to change the title of this category')
            title_change_description = T('Click to change the description of this category')
            title_change_name = T('Click to change the name of this category')
            title_delete = T('Click to remove this category')
            
            for cat in last_categories:
                
                if cat.description=="":
                    cat_description=T("No description")
                else:
                    cat_description=cat.description[:50]
                
                if cat.title=="":
                    cat_title = T("No title")
                else:
                    cat_title = cat.title[:50]
                
                if cat.name=="":
                    cat_name = T("No name")
                else:
                    cat_name = cat.name[:50]
                
                link_id = A(cat.id, _href='javascript: void(0);', \
                            _onclick="CategoryGoTo(%s);"%(cat.id))
                link_title = A(cat_title, _href='javascript: void(0);', \
                               _onclick="CategoryChangeTitle(%s);"%(cat.id), \
                               _title="%s"%title_change_title)
                link_description = A(cat_description, _href='javascript: void(0);', \
                                     _onclick="CategoryChangeDescription(%s);"%(cat.id), \
                                     _title="%s"%title_change_description)
                link_name = A(cat_name, _href='javascript: void(0);', \
                              _onclick="CategoryChangeName(%s);"%(cat.id), \
                              _title="%s"%title_change_name)
                icon_remove = IMG(_src=URL(request.application,'static','images/remove.png'), \
                                  _alt="remove")
                link_delete = A(icon_remove, _href='javascript: void(0);', \
                                _onclick="CategoryDelete(%s);"%(cat.id), \
                                _title="%s"%title_delete)                  
                
                row_column1 = '<div class="column1">%s</div>' % link_title.xml()
                row_column2 = '<div class="column2">%s</div>' % link_name.xml()
                row_column3 = '<div class="column3">%s</div>' % link_description.xml()
                row_column4 = '<div class="column4">%s</div>' % link_delete.xml()            
                
                row_clear = '<div style="clear: both;"></div>'
                
                row_comment_xml = '<div class="row-categories" id="row-%s"> %s %s %s %s %s </div>' \
                                % (cat.id,row_column1,row_column2,row_column3,row_column4,row_clear)
                list += row_comment_xml
                
            if count_categories>max_categories:
                total_pages = count_categories // max_categories
                if (count_categories % max_categories)>0:
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
                             _onclick="CategoryList(%s);"%(currentpage-1))           
                forward = A(T("Next"), _href='javascript: void(0);', \
                            _onclick="CategoryList(%s);"%(currentpage+1))
                
                listpages=""    
                if currentpage>1:
                    listpages += "<li>%s</li>" % backward.xml()                             
                
                for page in range(first_page, last_page+1):                
                    page_a = A(unicode(page), _href='javascript: void(0);', \
                               _onclick="CategoryList(%s);"%(page))
                    
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
            page_content=list + "%s"%T("No categories")    
        
                
        html_content = '<h2>%s</h2>'%T("Categories")
        html_content += "%s"%page_content
        info={}          
        info['html']=sanitate_string(html_content)
        return sj.dumps(info)        
    
    
    
    def add(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
         
        default_title = sanitate_string("%s"%T('No Title'))
        default_name = (IS_SLUG()("%s"%T('No Title')))[0]   
        #default_name = (IS_SLUG()(default_title))[0]
        newcat = db.categories.insert(title = default_title, name = default_name)    
        if newcat>0:        
            return json_response(message= T("Categorie added"),alert=0,value="")
        else:
            return json_response(message=T("The categorie id doesn't exist"),alert=2,value="")
        
    
        
    def delete(self, id):   
        
        db = self.i2p.db
        T = self.i2p.environment.T
             
        cats = db(db.categories.id == id).select()
        if cats:
            cat = cats[0]
            idcat = str(cat.id) #is a bug in web2py? contains only string?       
            countcat = db(db.posts.categories.contains(idcat)).count()
            if countcat>0:            
                return json_response(message=T('There are articles with this category'),\
                                     alert=2,value="")       
            else:
                db(db.categories.id == idcat).delete()            
                return json_response(message= T('Category deleted!'),\
                                     alert=0,value="")   
        else:
            return json_response(message= T("This category doesn't exist!"),\
                                 alert=2,value="")
        
            
    
    def change_title(self, id, value): 
        
        db = self.i2p.db
        T = self.i2p.environment.T        
                   
        categories = db(db.categories.id == id).select()
        if categories:
            cat = categories[0] 
            name = (IS_SLUG()(value))[0] #change also the name           
            if name!="":
                cat.update_record(title = value, name = name)         
                return json_response(message=  T("Title changed"),\
                                     alert=0,value="")     
            else:
                return json_response(message= T("The category name you enter is not valid!"),\
                                 alert=2,value="")         
        else:
            return json_response(message= T("This category doesn't exist!"),\
                                 alert=2,value="") 
        
    
        
    def get_title(self, id):
        
        db = self.i2p.db
        T = self.i2p.environment.T   
             
        categories = db(db.categories.id == id).select()
        if categories:
            cat = categories[0]
            value = cat.title
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message= T("This category doesn't exist!"),\
                                 alert=2,value="")
        
    
        
    def change_name(self, id, value): 
        
        db = self.i2p.db
        T = self.i2p.environment.T   
                
        categories = db(db.categories.id == id).select()
        if categories:
            cat = categories[0] 
            flat_name = (IS_SLUG()(value))[0] #change also the name       
            if flat_name!="":
                count = db(db.categories.name == flat_name).count()
                if count==0:              
                    cat.update_record(name = flat_name)                
                    return json_response(message= T("Name changed"),\
                                         alert=0,value="")
                else:                
                    return json_response(message= T("This name already exist in articles"),\
                                         alert=2,value="")
            else:                              
                return json_response(message= T("There is a problem with this name"),\
                                     alert=2,value="")
        else:        
            return json_response(message= T("This category doesn't exist!"),\
                                 alert=2,value="")
        
    
        
    def get_name(self, id):    
        
        db = self.i2p.db
        T = self.i2p.environment.T   
        
        categories = db(db.categories.id == id).select()
        if categories:
            cat = categories[0]
            value = cat.name        
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message= T("This category doesn't exist!"),\
                                 alert=2,value="")
        
    
    
    def change_description(self, id, value):
        
        db = self.i2p.db
        T = self.i2p.environment.T
                    
        categories = db(db.categories.id == id).select()
        if categories:    
            cat = categories[0]               
            cat.update_record(description = value)         
            return json_response(message=  T("Description changed"),\
                                 alert=0,value="")              
        else:
            return json_response(message= T("This category doesn't exist!"),\
                                 alert=2,value="")     
        
        
    
    def get_description(self, id):    
        
        db = self.i2p.db
        T = self.i2p.environment.T
         
        categories = db(db.categories.id == id).select()
        if categories:
            cat = categories[0]
            value = cat.description
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message= T("This category doesn't exist!"),\
                                 alert=2,value="")
 

     
    def _get_list_from_article(self, idpost): #_get_id_categories_from_article
        
        db = self.i2p.db
        
        categories=[]
        posts = db(db.posts.id == idpost).select()
        if posts:
            post = posts[0]
            if post.categories:
                categories =post.categories          
            
        return categories    
    

    def get_list_from_article(self, idpost):  #get_categories_from_article 
        
        db = self.i2p.db
        T = self.i2p.environment.T
            
        cat_from_article = self._get_list_from_article(idpost) #categories from article
        categories = self.i2p.categories.get_list() #all categories
        caption_title = T('Categories')
        id_form = 'catchange-form'
        id_submit = 'catchange-submit'  
        id_check = 'catchange-check'  
        if categories:
            options = ""
            for cat in categories:
                if cat.id in cat_from_article:
                    checked = 'checked'            
                else:
                    checked = ''                        
                
                option = '<li><input type="checkbox" value="%s" %s /> %s </li>' \
                            % (cat.id, checked, cat.title)
                options +=option      
                
            xml_ul = '<ul>%s</ul>' % (options)        
            xml = '<h2>%s</h2> <div style="height: 200px; overflow-y: scroll; "> %s </div>' \
                        % (caption_title,xml_ul)
            message=""
            alert=0
        else:
            xml = '<h2>%s</h2><ul>%s</ul>' % (caption_title, T("No categories"))
            message=T("No categories, create it before assigning!.")
            alert=1        
        
        return json_response(message,alert,value=xml)


    def _remove_from_article(self, id_post):
        db = self.i2p.db
        return db(db.categorieslist.post_id == id_post).delete()
    
    
    def _add_to_article(self, id_post, idcat):
        db = self.i2p.db   
        return db.categorieslist.insert(cat_id=idcat, post_id=id_post)  
    
    
    def _adds_to_article(self, id_post, categoriesList):
        db = self.i2p.db
        self._remove_from_article(id_post) #first remove all entries in article   
        for idcat in categoriesList:
            self._add_to_article(id_post, idcat)
    
    
    def _proper_list(self, value):
        db = self.i2p.db
        categoriesList=[]
        keywords = value.split(',')#first separate the keys
        for keyw in keywords:
            cleanKeyword = keyw.strip()
            if cleanKeyword=="":
                continue        
            try:
                intCategories = int(cleanKeyword)
            except:
                continue
            
            categories = db(db.categories.id ==  intCategories).select() #check if exist
            if categories:        
                categoriesList.append(intCategories)
            
        categoriesList = {}.fromkeys(categoriesList).keys() # Remove duplicate    
        
        return categoriesList
        
        
    def assign(self, postid, categories):  
        
        db = self.i2p.db
        T = self.i2p.environment.T
                  
        posts = db(db.posts.id == postid).select()
        if posts:
            post = posts[0]        
            categoriesList = self._proper_list(categories)        
            try:            
                post.update_record(categories = categoriesList) 
                self._adds_to_article(postid, categoriesList)
            except:
                db.rollback()                
                return json_response(message=T("Problem saving categories"),\
                                     alert=2,value="")        
            else:
                db.commit()           
                return json_response(message=T("Article categories was updated!"),\
                                     alert=0,value="")        
                  
        else:
            return json_response(message=T("The article id doesn't exist"),\
                                 alert=2,value="")
              
      