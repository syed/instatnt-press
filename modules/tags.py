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

import datetime

from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *
from gluon.sql import *
import gluon.contrib.simplejson as sj

#local
from utils import *



class Tags(object): 
    
    def __init__(self, i2p):
        
        self.i2p = i2p        
        
    
    
    def define_tables(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        
        db.define_table('tags',                                  
            Field('id', 'id'),
            Field('name', 'string', length=512, requires=(IS_SLUG())),     
            Field('title', 'string', length=512, required=True),                                 
            Field('created_on', 'datetime', default=datetime.datetime.today()),                                                                                                                            
            migrate=self.i2p.config.is_first_time)
        
        db.define_table('tagslist',                                  
            Field('id', 'id'),
            Field('tag_id', 'integer', required=True),     
            Field('post_id', 'integer', required=True),                                                                                                                         
            migrate=self.i2p.config.is_first_time)
        
        db.tagslist.tag_id.requires = IS_IN_DB(db, 'tags.id', 'tags.title')
        db.tagslist.post_id.requires = IS_IN_DB(db, 'posts.id', 'posts.title')



class admTags(object): 
    
    
    def __init__(self, i2p):
        
        self.i2p = i2p
        

    def _remove_from_article(self, id_post):
        
        db = self.i2p.db
                
        tagslist = db(db.tagslist.post_id == id_post).select()
        for tag_entry in tagslist:
            tag_id = tag_entry.tag_id
            count = db(db.tagslist.tag_id == tag_id).count()
            if count <= 1:
                db(db.tags.id == tag_id).delete() #delete the description if there are only entry
        db(db.tagslist.post_id == id_post).delete()
    
    
    def _add_new_keyword(self, name, title):
        
        db = self.i2p.db
                
        tags = db(db.tags.name==name).select()
        if tags:
            return tags[0].id
        else:              
            id_tag= db.tags.insert(name=name, title=title)        
            return id_tag
    
    
    def _add_keyword(self, id_post, key):
        
        db = self.i2p.db
                
        name = (IS_SLUG()(key))[0] #_utils_flat_title(key)    
        idtag = self._add_new_keyword(name,key)
        new_entry = db.tagslist.insert(tag_id=idtag, post_id=id_post)  
    
    
    def save_keywords_as_tags(self, id_post, keywordsList):
        
        db = self.i2p.db
                
        self._remove_from_article(id_post) #first remove all entries in tags with post   
        for key in keywordsList:
            self._add_keyword(id_post, key)

