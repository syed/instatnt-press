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

from gluon.storage import *

class Instant2Press(object): 
    
    def __init__(self, environment, db, config):
        
        self.environment = Storage(environment)        
        self.db = db
        self.config = config
       
    def define_categories(self):
        
        db = self.db
        if not hasattr(db, 'categories'):        
            self.categories.define_tables()
    
    def define_articles(self):
        
        db = self.db
        if not hasattr(db, 'posts'):        
            self.articles.define_tables() 
        
    def define_comments(self):
        
        db = self.db
        if not hasattr(db, 'comments'):        
            self.comments.define_tables() 
    
    def define_tags(self):
        
        db = self.db
        if not hasattr(db, 'tags'):
            self.tags.define_tables()  
    
    def define_links(self):
        
        db = self.db
        if not hasattr(db, 'links'):        
            self.links.define_tables()     
        
    def define_styles(self):
        
        db = self.db
        if not hasattr(db, 'style'): 
            self.styles.define_tables()
        
    def define_images(self):
        
        db = self.db
        if not hasattr(db, 'images'):
            self.images.define_tables()
        
    def define_avatars(self):
        
        db = self.db
        if not hasattr(db, 'avatars'):
            self.avatars.define_tables()
        
    def define_siteinfo(self):
        
        db = self.db
        if not hasattr(db, 'siteinfo'):                        
            self.siteinfo.define_tables()    

    def load_mod_users(self):
        
        if not hasattr(self, 'users'):                
            mod_users = local_import("users")
            self.users = mod_users.Users(self)
    
    def load_mod_users_admin(self):
        
        if not hasattr(self, 'admin_users'):                
            mod_users = local_import("users")
            self.admin_users = mod_users.admUsers(self)        
        
    def load_mod_filldb(self):
        
        if not hasattr(self, 'filldb'):
            mod_filldb = local_import("filldb")
            self.filldb = mod_filldb.FillData(self)
            
    def load_mod_categories(self):
        
        if not hasattr(self, 'categories'):
            mod_categories = local_import("categories") 
            self.categories = mod_categories.Categories(self)

    def load_mod_categories_admin(self):
        
        if not hasattr(self, 'admin_categories'):
            mod_categories = local_import("categories") 
            self.admin_categories = mod_categories.admCategories(self)

                
    def load_mod_articles(self):
        
        if not hasattr(self, 'articles'):
            mod_articles = local_import("articles")
            self.articles = mod_articles.Articles(self)
    
    def load_mod_articles_admin(self):
        
        if not hasattr(self, 'admin_articles'):
            mod_articles = local_import("articles")
            self.admin_articles = mod_articles.admArticles(self)        
            
    def load_mod_tags(self):
        
        if not hasattr(self, 'tags'):
            mod_tags = local_import("tags")
            self.tags = mod_tags.Tags(self)

    def load_mod_tags_admin(self):
        
        if not hasattr(self, 'admin_tags'):
            mod_tags = local_import("tags")
            self.admin_tags = mod_tags.admTags(self)
        
            
    def load_mod_comments(self):
        
        if not hasattr(self, 'comments'):
            mod_comments = local_import("comments") 
            self.comments = mod_comments.Comments(self)
            
    
    def load_mod_comments_admin(self):
        
        if not hasattr(self, 'admin_comments'):
            mod_comments = local_import("comments") 
            self.admin_comments = mod_comments.admComments(self)
    
            
    def load_mod_links(self):
        
        if not hasattr(self, 'links'):
            mod_links = local_import("links")
            self.links = mod_links.Links(self)
            
    
    def load_mod_links_admin(self):
        
        if not hasattr(self, 'admin_links'):
            mod_links = local_import("links")
            self.admin_links = mod_links.admLinks(self)
        
            
    def load_mod_styles(self):
        
        if not hasattr(self, 'styles'):
            mod_styles = local_import("styles") 
            self.styles = mod_styles.Styles(self)
    
    def load_mod_styles_admin(self):
        
        if not hasattr(self, 'admin_styles'):
            mod_styles = local_import("styles") 
            self.admin_styles = mod_styles.admStyles(self)
                
    def load_mod_images(self):
        
        if not hasattr(self, 'images'):
            mod_images = local_import("images") 
            self.images = mod_images.Images(self)        
            self.avatars = mod_images.Avatars(self)
    
    def load_mod_images_admin(self):
        
        if not hasattr(self, 'admin_images'):
            mod_images = local_import("images") 
            self.admin_images = mod_images.admImages(self)        
            
                
    def load_mod_siteinfo(self):  
        
        if not hasattr(self, 'siteinfo'):
            mod_siteinfo = local_import("siteinfo") 
            self.siteinfo = mod_siteinfo.SiteInfo(self)
    
    
    def load_mod_siteinfo_admin(self):  
        
        if not hasattr(self, 'admin_info'):
            mod_siteinfo = local_import("siteinfo") 
            self.admin_info = mod_siteinfo.admSiteInfo(self)
              
    
    def load_mod_widgets(self):
        
        if not hasattr(self, 'widgets'):
            mod_widgets = local_import("widgets") 
            self.widgets = mod_widgets.Widgets(self)
    
    
    def load_mod_common(self):
                
        self.load_mod_users()
        self.load_mod_siteinfo()
        self.load_mod_articles()
        self.load_mod_categories()        
        self.load_mod_tags()
        self.load_mod_comments()
        self.load_mod_links()
        self.load_mod_styles()
        self.load_mod_images()
        self.load_mod_widgets()

    def load_mod_common_admin(self):
                
        self.load_mod_users_admin()
        self.load_mod_siteinfo_admin()
        self.load_mod_categories_admin()
        self.load_mod_articles_admin()
        self.load_mod_tags_admin()
        self.load_mod_comments_admin()
        self.load_mod_links_admin()
        self.load_mod_styles_admin()
        self.load_mod_images_admin()
               
    
    def db_definitions(self):
        
        self.define_siteinfo()        
        self.define_articles()
        self.define_categories()
        self.define_tags()
        self.define_comments()
        self.define_links()
        self.define_styles()
        self.define_images()
        self.define_avatars()
        
        
                
                
        