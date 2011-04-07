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
from fulltext import *

SEARCH_MAX_WORDS=10

ADMIN_MAX_LIST_PAGES = 10
ADMIN_POST_LIST_PER_PAGE = 5
POST_LIST_PER_PAGE = 5

POST_PUBLISHED = 1
POST_IS_PAGE = 1
POST_IS_NOT_PAGE = 0

RSS_MAX_POSTS = 20
RSS_MAX_COMMENTS = 20
POPULAR_TAGS_LIMIT = 40


class Articles(object): 
    
    def __init__(self, i2p):
        
        self.i2p = i2p      
        
        
    
    def define_tables(self):
        
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request        
        fulltext_field = self.i2p.config.fulltext_field   
        config = self.i2p.config     
        
        db.define_table('posts',                                  
            Field('id', 'id'),
            Field('name', 'string', length=255, default="",requires=(IS_SLUG())), 
            Field('title', 'string', length=255, required=True),                                      
            Field('description', 'text', default=""),
            Field('text_slice', 'text', default=""),                                    
            Field('keywords', 'list:string'), #tags                  
            Field('categories', 'list:reference categories'),                  
            Field('created_on', 'datetime', default=datetime.datetime.today()),
            Field('published_on', 'datetime', default=datetime.datetime.today()),
            Field('updated_on', 'datetime', default=datetime.datetime.today()),
            Field('created_by_id', 'integer', default=0, required=True),
            Field('updated_by_id', 'integer', default=0, required=True),
            Field('created_by_name', 'string', length=255, default=""), #not used but in gae 
                                                                        #put author name here
            Field('updated_by_name', 'string', length=255, default=""), #not used but in gae 
                                                                        #put author name here                                     
            Field('published', 'integer', default=0, required=True),
            Field('is_page', 'integer', default=0, required=True),
            Field('page_order', 'integer', default=0),
            Field(fulltext_field, 'list:string'), #OMG: In mysql cannot be a field called 
                                                  #fulltext, rename to full_text
            Field('post_url', 'text', default="", requires=(IS_URL())),                                                                                         
            migrate=config.is_first_time)
        
        db.posts.published.requires = IS_IN_SET(['0', '1'])
        db.posts.is_page.requires = IS_IN_SET(['0', '1'])
    
    

    def _get_post_title(self, id):
        
        db = self.i2p.db
        
        title = "No title"
        posts = db(db.posts.id==id).select()
        if posts:
            title = posts[0].title
            
        return title  
     
     

    def get_all_categories(self):
        
        db = self.i2p.db
              
        categories = db(db.categories.id>0).select(db.categories.ALL, \
                                                   orderby=db.categories.title)
        return categories



    def get_post_category(self, id):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        config = self.i2p.config
           
        xml_cats = ""
        posts = db(db.posts.id == id).select()
        if posts:
            post = posts[0]
            list_categories = post.categories
            if list_categories:
                for cat_id in list_categories:            
                    categories = db(db.categories.id == cat_id).select()
                    if categories:
                        cat = categories[0]
                        cat_title = A(cat.title, \
                                      _href=URL(request.application, \
                                                config.controller_default, \
                                                'category/by_id', \
                                                args=[unicode(cat.id)] ))
                        xml_cats += " %s " % cat_title.xml()
          
        return xml_cats 
    
    

    def _get_query_publish_post(self):
        
        db = self.i2p.db
        
        query = (db.posts.published==POST_PUBLISHED) & \
                (db.posts.is_page==POST_IS_NOT_PAGE)
                
        return query  



    def _get_query_publish_page(self):
        
        db = self.i2p.db
        
        query = (db.posts.published==POST_PUBLISHED) & \
                (db.posts.is_page==POST_IS_PAGE)
                
        return query
    
        

    def get_page_permanent_link(self, id, title="", anchor=""):
            
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        config = self.i2p.config
        
        page_title = ""
        posts = db((db.posts.id == id) & \
                   (db.posts.is_page==POST_IS_PAGE)).select()    
        if posts:
            post = posts[0]
            if post.name != "":
                #permanent link with post like: page/my-name-is-carl                        
                permanent = 'page' + '/' + post.name
                if title=="":
                    title = post.title
                page_title = A(title, _href=URL(request.application, \
                                                config.controller_default, \
                                                permanent,anchor=anchor))            
            else:
                #permanent link with default view
                if title=="":
                    title = post.title
                page_title = A(title, _href=URL(request.application, \
                                                config.controller_default, \
                                                'page_by_id', \
                                                args=[unicode(post.id)], \
                                                anchor=anchor ))
            
        return page_title
    
       

    def get_post_permanent_link(self, id, title="", anchor="", \
                                trunk=False, only_url=False, full=False):
        
                
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        config = self.i2p.config
        
        post_title = ""
        post_url = ""
        posts = db(db.posts.id == id).select()    
        if posts:
            post = posts[0]
            if post.name != "":
                current_name = post.name
                count_name = db(db.posts.name == current_name).count()
                if count_name > 1: #another with the same name?
                    if title=="":
                        if trunk:
                            title = post.title[:50]
                        else:
                            title = post.title
                    post_url = URL(request.application,\
                                   config.controller_default,'view', \
                                   args=[unicode(post.id),current_name], \
                                   anchor=anchor )
                    post_title = A(title, _href=post_url)
                else:            
                    #permanent link with post like: post/2010/07/01/my-name-is-carl
                    year = post.published_on.strftime("%Y")
                    month = post.published_on.strftime("%m")
                    day = post.published_on.strftime("%d")            
                    permanent = 'post' + '/' + year + "/" + month + "/" + day + '/' + post.name
                    if title=="":
                        if trunk:
                            title = post.title[:50]
                        else:
                            title = post.title
                    
                    if config.short_url:
                        if anchor!="":
                            url_anchor= '#' + anchor
                        else:
                            url_anchor = ''
                        post_url = 'http://' + str(request.env.http_host) + '/' + \
                                    request.application + '/' +year + "/" + month + \
                                    "/" + day + '/' + post.name + url_anchor                   
                    else:
                        post_url = URL(request.application, \
                                       config.controller_default, \
                                       permanent, anchor=anchor)
                        
                    post_title = A(title, _href=post_url)            
            else:
                #permanent link with default view
                if title=="":
                    if trunk:
                        title = post.title[:50]
                    else:
                        title = post.title
                
                post_url = URL(request.application, \
                               config.controller_default, \
                               'view', \
                               args=[unicode(post.id)], \
                               anchor=anchor )
                post_title = A(title, _href=post_url)
        
        if full and not config.short_url:
            post_url = 'http://%(http_host)s/%(post_url)s' % {'http_host': request.env.http_host,\
                                                              'post_url': post_url} 
            
        
        if only_url:
            return post_url
        else:        
            return post_title



  
    def get_popular_tags(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        config = self.i2p.config
        
        def most_common_words(items):
            from string import punctuation    
            words = {}    
            words_gen = (word.strip(punctuation).lower() for word in items)    
            for word in words_gen:
                words[word] = words.get(word, 0) + 1        
            top_words = sorted(words.iteritems(),key=lambda(word, count): (-count, word))
            return top_words
    
        xml_tags=''
        limit_tags = POPULAR_TAGS_LIMIT
        query = self._get_query_publish_post() #basic query
        posts = db(query).select(db.posts.ALL, \
                                 orderby=~db.posts.published_on)
        
        list_tags=[]    
        for post in posts:
            if post.keywords:
                keywords = post.keywords
                for key in keywords:
                    list_tags.append(key) #all tags in a list
        
        if list_tags!=[]:                            
            common_tags = most_common_words(list_tags)[:limit_tags]    
            for word in common_tags:
                tag = word[0]
                name = (IS_SLUG()(tag))[0]
                link_search = A(tag, _href=URL(request.application, \
                                               config.controller_default, \
                                               'tag', \
                                               args=[name]))             
                xml_tags += '<li>%s</li>' % link_search.xml()
               
            tags_caption = T('Popular Tags')    
            if xml_tags!='':
                xml_tags = '<div id="popular-tags"><h2>%s</h2><ul>%s</ul></div>' % \
                (tags_caption,xml_tags)
            
        return xml_tags



    def get_list_links(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
         
        xml_links='' 
        link_list=''    
        links = db(db.links.id>0).select()
        for link in links:
            link_link =  A(link.title, \
                           _href=link.url, \
                           _title=link.description)
            
            link_list += '<li>%s</li>'% link_link
                
        if link_list!='':
            link_caption = T('Links')
            xml_links = '<h2>%s</h2><ul>%s</ul>' % (link_caption, link_list)
        
        return xml_links



    #if you wanna try:
    #change in sqlite similar like dis:
    #update posts set created_on="2010-08-08 11:54:01",  published_on="2010-08-08 11:54:01", updated_on="2010-08-08 11:54:01" where id=1;
    def get_list_archives(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        xml_archive=''        
        query = self._get_query_publish_post() #basic query
        posts = db(query).select(db.posts.ALL, \
                                 orderby=~db.posts.published_on)
        calendar_list=[] 
        archive_list=""    
        for post in posts:
            year_full = post.published_on.strftime("%Y")
            month_full = post.published_on.strftime("%B")
            month = post.published_on.strftime("%m")
            month_year = "%s %s" % (year_full,month_full)
            if month_year not in calendar_list:
                calendar_list.append(month_year)
                link_month = A(month_year, _href=URL(request.application, \
                                                     self.i2p.config.controller_default, \
                                                     'archives', \
                                                     args=[year_full,month]))
                archive_list += '<li>%s</li>'% link_month
            
        if archive_list!='':
            archive_caption = T('Archives')
            xml_archive = '<h2>%s</h2><ul>%s</ul>' % (archive_caption, archive_list)
        
        return xml_archive
    
    
      

    #now only get the article with the name
    def get_article_id_from_date_name(self, year, month, day, name):
        return self.get_article_id_from_name(name) 



    
    def get_article_id_from_name(self, name): 
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        id_post = 0
        query = (db.posts.name==name)
        posts = db(query).select()
        if posts:
            id_post = posts[0].id
            
        return id_post
    
    
  
    def get_last_posts_with_tag_name(self, page, tag):  
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
            
        (limit_inf, limit_sup) = get_query_limits(page, POST_LIST_PER_PAGE)    
        query = self._get_query_publish_post() #basic query
        tag = tag.replace("-"," ")#replace - with space        
        query = query & (db.posts.keywords.contains(tag)) #bug web2py, fix in trunk
        last_posts_count = db(query).count()
        last_posts = db(query).select(db.posts.ALL, \
                                      orderby=~db.posts.published_on, \
                                      limitby=(limit_inf, limit_sup))
            
        return (last_posts, last_posts_count)



    def get_last_posts_with_cat_id(self, page, category):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
             
        (limit_inf, limit_sup) = get_query_limits(page, POST_LIST_PER_PAGE)    
        query = self._get_query_publish_post() #basic query   
        query = query & (db.posts.categories.contains(category)) #bug web2py, fix in trunk
        last_posts_count = db(query).count()
        last_posts = db(query).select(db.posts.ALL, \
                                      orderby=~db.posts.published_on, \
                                      limitby=(limit_inf, limit_sup))
            
        return (last_posts, last_posts_count)
    
    
    

    def get_last_posts(self, page=1): 
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
            
        (limit_inf, limit_sup) = get_query_limits(page, POST_LIST_PER_PAGE)
        query = self._get_query_publish_post() #basic query    
        last_posts_count = db(query).count()
        last_posts = db(query).select(db.posts.ALL, \
                                      orderby=~db.posts.published_on, \
                                      limitby=(limit_inf, limit_sup))
        
        return (last_posts, last_posts_count)



    def get_last_pages(self, page=1):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
             
        (limit_inf, limit_sup) = get_query_limits(page, POST_LIST_PER_PAGE)    
        query = self._get_query_publish_page()
        last_posts_count = db(query).count()
        last_posts = db(query).select(db.posts.ALL, \
                                      orderby=~db.posts.published_on, \
                                      limitby=(limit_inf, limit_sup))
        
        return (last_posts, last_posts_count)
    
    

    def get_last_posts_archives_monthyear(self, page=1, year=2010, month=8):
        
        import datetime
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request  
        
          
        def last_day_of_month(date):
            if date.month == 12:
                return date.replace(day=31)
            return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)
     
        (limit_inf, limit_sup) = get_query_limits(page, POST_LIST_PER_PAGE)    
        query = self._get_query_publish_post()
        
        d_lower=datetime.datetime(year,month,1) 
        d_upper=last_day_of_month(d_lower)     
        
        query = query & (db.posts.published_on>=d_lower) & \
                (db.posts.published_on<=d_upper)
                
        last_posts_count = db(query).count()
        last_posts = db(query).select(db.posts.ALL, \
                                      orderby=db.posts.published_on, \
                                      limitby=(limit_inf, limit_sup))
        
        return (last_posts, last_posts_count)
    
    
    

    def get_last_posts_with_search(self, page, textSearch):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request  
        
        (limit_inf, limit_sup) = get_query_limits(page, POST_LIST_PER_PAGE)
        
        search_list = textSearch.split()
        clean_list = []    
        for word in search_list:
            cleanword = word.strip()
            if cleanword=="":
                continue
            
            cleanword = cleanword.lower()
                        
            if len(cleanword)<=1:
                continue     
            
            clean_list.append(cleanword)    
         
        clean_list = {}.fromkeys(clean_list).keys() # Remove duplicate
        try: clean_list.remove('') 
        except: pass #remove '' 
        
        clean_list = clean_list[:SEARCH_MAX_WORDS] #trunc max words to search
            
        query = self._get_query_publish_post() #basic query
        
        fulltext_field = self.i2p.config.fulltext_field
        
        #contains: Bug web2py. Need to fix this
        if request.env.web2py_runtime_gae:
            if isinstance(clean_list, list ):
                query = query & (db.posts[fulltext_field].contains(clean_list))            
        else:
            for search_word in clean_list: 
                if isinstance(search_word, (unicode, str) ):
                    query = query & (db.posts[fulltext_field].contains(search_word)) 
     
            
        last_posts = db(query).select(db.posts.ALL, 
                                      orderby=~db.posts.published_on, 
                                      limitby=(limit_inf, limit_sup))
        
        last_posts_count = db(query).count()                    
            
        return (last_posts, last_posts_count)    
    
    

    def get_xml_results_from_posts(self, posts):
        
        xml_posts=''
        for post in posts:            
            xml_posts += self.i2p.widgets.post_extract(post)
        
        return xml_posts


   
   
    def get_article_view_by_id(self, post_id, preview=False):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        post=None        
        query = (db.posts.id == post_id) 
        if not preview:
            query = query & (db.posts.published==POST_PUBLISHED)
        posts = db(query).select()
        if posts:
            post=posts[0]
                           
        return post




    def keywords_to_tags_link(self, keywords):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        xml=''
        #keywords = _keywords_to_proper_list(values)
        if keywords:
            for key in keywords:            
                name = (IS_SLUG()(key))[0]
                link = A(key, _href=URL(request.application, \
                                        self.i2p.config.controller_default, \
                                        'tag', \
                                         args=[name] ))
                xml +=" " + link.xml()
                    
        return xml
    
    

    #generate rss of the lastest posts                
    def generate_rss_last_posts(self, page=1, full_content=False):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
            
        entries=[]
        base_http = 'http://' + str(request.env.http_host)
        (limit_inf, limit_sup) = get_query_limits(page, RSS_MAX_POSTS)
        query = self._get_query_publish_post()    
        last_posts = db(query).select(db.posts.ALL, \
                                      orderby=~db.posts.published_on, \
                                      limitby=(limit_inf, limit_sup))
        for post in last_posts:
            title_post = post.title        
            url_post = str(base_http + \
                           self.get_post_permanent_link(post.id,only_url=True))        
            if full_content:
                description_post = post.description
            else:
                description_post = post.text_slice  
            published_on = str(post.published_on)                    
            rss_post = dict(title=title_post,
                            link=url_post,
                            description=description_post,
                            created_on=published_on)
            entries.append(rss_post)
        
        #site properties
        title_site = self.i2p.siteinfo._get_title()
        url_site = str(base_http + URL(request.application, \
                                       self.i2p.config.controller_default, \
                                       'index'))
        description_site = self.i2p.siteinfo._get_description()
        feed = dict(title=title_site,
                    link=url_site,
                    description=description_site,
                    entries=entries)    
        
        return feed
    
        

    #generate rss of the lastest comments                
    def generate_rss_last_comments(self, page=1, full_content=False):  
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
          
        entries=[]
        base_http = 'http://' + str(request.env.http_host)
        (limit_inf, limit_sup) = get_query_limits(page, RSS_MAX_COMMENTS)
        query = (db.comments.id>0)    
        last_comments = db(query).select(db.comments.ALL, \
                                         orderby=~db.comments.comment_on, \
                                         limitby=(limit_inf, limit_sup))
        for comment in last_comments:
            comment_user = self.i2p.users.get_user_title(comment.author_id)
            title_post = self._get_post_title(comment.post_id)       
            url_post = str(base_http + \
                           self.get_post_permanent_link(comment.post_id, \
                                                        anchor="comments", \
                                                        only_url=True))
                    
            comment_text = '%s Says: %s' % (comment_user,comment.comment[:250])  
            comment_on = str(comment.comment_on)                    
            rss_comment = dict(title=title_post,
                            link=url_post,
                            description=comment_text,                        
                            created_on=comment_on)
            entries.append(rss_comment)
        
        #site properties
        title_site = self.i2p.siteinfo._get_title()
        url_site = str(base_http + URL(request.application, \
                                       self.i2p.config.controller_default, \
                                       'index'))
        
        description_site = self.i2p.siteinfo._get_description()
        feed = dict(title=title_site,
                    link=url_site,
                    description=description_site,
                    entries=entries)    
        
        return feed


    #get_xml_next_pages_from_last_post
    def pagination_last_post(self, currentpage, \
                             count, \
                             max_list_per_page=POST_LIST_PER_PAGE, \
                             max_display_pages=10):
                
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        list=''    
        if count>max_list_per_page:
            total_pages = count // max_list_per_page
            if (count % max_list_per_page)>0:
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
                    
            backward=A(T("Prior"), _href=URL(request.application, \
                                             self.i2p.config.controller_default, \
                                             'index', \
                                             args=[unicode(currentpage-1)] ))           
            forward=A(T("Next"), _href=URL(request.application, \
                                           self.i2p.config.controller_default, \
                                           'index', \
                                           args=[unicode(currentpage+1)] ))
                    
            listpages=""    
            if currentpage>1:
                listpages += "<li>%s</li>" % backward.xml()                             
            
            for page in range(first_page, last_page+1):      
                page_a=A(str(page), _href=URL(request.application, \
                                              self.i2p.config.controller_default, \
                                              'index',args=[unicode(page)] ))                        
                if page<=total_pages:
                    if page==currentpage:
                        class_current = ' class="current"'
                    else:
                        class_current = '' 
                    listpages += "<li%s>%s</li>" % (class_current, page_a.xml())            
                
            if total_pages>currentpage:
                listpages += "<li>%s</li>" % forward.xml()
            
            if listpages!="":                  
                list='<div class="pages"><ul>%s</ul></div>' % (listpages)
        
        return list



    #get_xml_next_pages_from_last_post_cat
    def pagination_last_post_cat(self, currentpage, \
                                 count, category, \
                                 max_list_per_page=POST_LIST_PER_PAGE, \
                                 max_display_pages=10):
                        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        list=''    
        if count>max_list_per_page:
            total_pages = count // max_list_per_page
            if (count % max_list_per_page)>0:
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
                    
            backward=A(T("Prior"), _href=URL(request.application, \
                                             self.i2p.config.controller_default, \
                                             'category/by_id', args=[unicode(category)], \
                                             vars={'page': unicode(currentpage-1)}))           
            forward=A(T("Next"), _href=URL(request.application, \
                                           self.i2p.config.controller_default, \
                                           'category/by_id', \
                                           args=[unicode(category)], \
                                           vars={'page': unicode(currentpage+1)}))
                    
            listpages=""    
            if currentpage>1:
                listpages += "<li>%s</li>" % backward.xml()                             
            
            for page in range(first_page, last_page+1):            
                page_a=A(str(page), _href=URL(request.application, \
                                              self.i2p.config.controller_default, \
                                              'category/by_id', \
                                              args=[unicode(category)], \
                                              vars={'page': unicode(page)}))                        
                if page<=total_pages:
                    if page==currentpage:
                        class_current = ' class="current"'
                    else:
                        class_current = '' 
                    listpages += "<li%s>%s</li>" % (class_current, page_a.xml())            
                
            if total_pages>currentpage:
                listpages += "<li>%s</li>" % forward.xml()
            
            if listpages!="":                  
                list='<div class="pages"><ul>%s</ul></div>' % (listpages)
        
        return list



    #get_xml_next_pages_from_last_post_tag
    def pagination_last_post_tag(self, currentpage, \
                                 count, tag, \
                                 max_list_per_page=POST_LIST_PER_PAGE, \
                                 max_display_pages=10):
        
                
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        list=''    
        if count>max_list_per_page:
            total_pages = count // max_list_per_page
            if (count % max_list_per_page)>0:
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
            
            
            backward=A(T("Prior"), _href=URL(request.application, \
                                             self.i2p.config.controller_default, \
                                             'tag', \
                                             args=[tag], \
                                             vars={'page': unicode(currentpage-1)}))           
            forward=A(T("Next"), _href=URL(request.application, \
                                           self.i2p.config.controller_default, \
                                           'tag', \
                                           args=[tag], \
                                           vars={'page': unicode(currentpage+1)} ))
                    
            listpages=""    
            if currentpage>1:
                listpages += "<li>%s</li>" % backward.xml()                             
            
            for page in range(first_page, last_page+1):            
                page_a=A(str(page), _href=URL(request.application, \
                                              self.i2p.config.controller_default, \
                                              'tag', \
                                              args=[tag], \
                                              vars={'page': unicode(page)} ))                        
                if page<=total_pages:
                    if page==currentpage:
                        class_current = ' class="current"'
                    else:
                        class_current = '' 
                    listpages += "<li%s>%s</li>" % (class_current, page_a.xml())            
                
            if total_pages>currentpage:
                listpages += "<li>%s</li>" % forward.xml()
            
            if listpages!="":                  
                list='<div class="pages"><ul>%s</ul></div>' % (listpages)
        
        return list



    #get_xml_next_pages_from_archive_monthyear
    def pagination_archive_monthyear(self, currentpage, \
                                     count, year, \
                                     month, \
                                     max_list_per_page=POST_LIST_PER_PAGE, \
                                     max_display_pages=10):
        
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        list=''    
        if count>max_list_per_page:
            total_pages = count // max_list_per_page
            if (count % max_list_per_page)>0:
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
            
            
            backward=A(T("Prior"), _href=URL(request.application, \
                                             self.i2p.config.controller_default, \
                                             'archives', \
                                             args=[year,month], \
                                             vars={'page': unicode(currentpage-1)}))           
            forward=A(T("Next"), _href=URL(request.application, \
                                           self.i2p.config.controller_default, \
                                           'archives', \
                                           args=[year,month], \
                                           vars={'page': unicode(currentpage+1)} ))
                    
            listpages=""    
            if currentpage>1:
                listpages += "<li>%s</li>" % backward.xml()                             
            
            for page in range(first_page, last_page+1):            
                page_a=A(str(page), _href=URL(request.application, \
                                              self.i2p.config.controller_default, \
                                              'archives', \
                                              args=[year,month], \
                                              vars={'page': unicode(page)} ))                        
                if page<=total_pages:
                    if page==currentpage:
                        class_current = ' class="current"'
                    else:
                        class_current = '' 
                    listpages += "<li%s>%s</li>" % (class_current, page_a.xml())            
                
            if total_pages>currentpage:
                listpages += "<li>%s</li>" % forward.xml()
            
            if listpages!="":                  
                list='<div class="pages"><ul>%s</ul></div>' % (listpages)
        
        return list



    #get_xml_next_pages_from_last_post_search
    def pagination_last_post_search(self, currentpage, \
                                    count, qvalue, \
                                    max_list_per_page=POST_LIST_PER_PAGE, \
                                    max_display_pages=10):
                
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        list=''    
        if count>max_list_per_page:
            total_pages = count // max_list_per_page
            if (count % max_list_per_page)>0:
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
                    
            backward=A(T("Prior"), _href=URL(request.application, \
                                             self.i2p.config.controller_default, \
                                             'search', \
                                             vars={'page': unicode(currentpage-1), 'q': qvalue}))           
            forward=A(T("Next"), _href=URL(request.application, \
                                           self.i2p.config.controller_default, \
                                           'search', \
                                           vars={'page': unicode(currentpage+1), 'q': qvalue} ))
                    
            listpages=""    
            if currentpage>1:
                listpages += "<li>%s</li>" % backward.xml()                             
            
            for page in range(first_page, last_page+1):            
                page_a=A(str(page), _href=URL(request.application, \
                                              self.i2p.config.controller_default, \
                                              'search', vars={'page': unicode(page), 'q': qvalue}  ))                        
                if page<=total_pages:
                    if page==currentpage:
                        class_current = ' class="current"'
                    else:
                        class_current = '' 
                    listpages += "<li%s>%s</li>" % (class_current, page_a.xml())            
                
            if total_pages>currentpage:
                listpages += "<li>%s</li>" % forward.xml()
            
            if listpages!="":                  
                list='<div class="pages"><ul>%s</ul></div>' % (listpages)
        
        return list
    
    
    
  

    
class admArticles(object): 
    
    def __init__(self, i2p):
        
        self.i2p = i2p    
    
        
    def list(self, currentpage=1, search_text=""):        
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        if not isinstance(search_text, (unicode, str) ): 
            search_text = ""
    
        max_posts=ADMIN_POST_LIST_PER_PAGE
        max_display_pages=ADMIN_MAX_LIST_PAGES
        
        limit_inf = (max_posts * currentpage) - max_posts
        limit_sup = limit_inf + max_posts 
        
        query = (db.posts.id>0) 
        if search_text!="":
            query = query & (db.posts.title.like(search_text+"%"))
        count_posts = db(query).count()
        last_posts = db(query).select(db.posts.ALL, \
                                      orderby=~db.posts.published_on, \
                                      limitby=(limit_inf, limit_sup))
    
        new_post = A(T("Add"), _href='javascript: void(0);', \
                     _onclick="ArticleAdd();", \
                     _title="%s"%T('Create new article'))  
        
        icon_post_url = URL(request.application, \
                            'static', \
                            'images/toolbar_add.png')   
         
        toolbar_new_post_style = 'padding-left: 20px; background-image: url(%s); background-repeat: no-repeat;' \
                                  % icon_post_url
        
        refresh_list = A(T("Refresh"), _href='javascript: void(0);', \
                         _onclick="ArticleList(1);", \
                         _title="%s"%T('Reload the list'))
        
        icon_refresh_url = URL(request.application, \
                               'static', \
                               'images/toolbar_refresh.png')
            
        toolbar_refresh_style = 'padding-left: 20px; background-image: url(%s); background-repeat: no-repeat;' \
                                % icon_refresh_url
        
        input_search = '<input type="text" id="input-search" style="width: 200px; height: 20px; margin: 0px;" />'
        icon_search_url = URL(request.application,'static','images/search.png')
        icon_search = IMG(_src=icon_search_url, _alt="search")
        do_search = A(icon_search, _href='javascript: void(0);', \
                      _onclick="ArticleSearch();", \
                      _title="%s"%T('Search in title'))
            
        toolbar_new_post = '<li style="%s">%s</li>' % (toolbar_new_post_style,new_post.xml())
        toolbar_refresh = '<li style="%s">%s</li>' % (toolbar_refresh_style,refresh_list.xml())
        toolbar_input_search = '<li>%s %s</li>' % (input_search, do_search.xml())
        
        toolbar = '<ul>%s %s %s</ul>' % (toolbar_new_post,toolbar_refresh,toolbar_input_search)    
        list = '<div class="toolbar" style="height: 40px; width: 500px;">%s</div>' % toolbar        
           
        if last_posts:  
            
            #create the header column   
            caption_column1 = T('Title')
            caption_column2 = T('Content')
            caption_column3 = T('Extract')
            caption_column4 = T('Cats')
            caption_column5 = T('Tags')
            caption_column6 = T('Public')
            caption_column7 = T('Page') 
            caption_column8 = T('PageUrl')        
            caption_column9 = T('Name')
            caption_column10 = T('Act')
            caption_column11 = T('Updated')
            
            row_column1 = '<div class="column1">%s</div>' % caption_column1
            row_column2 = '<div class="column2">%s</div>' % caption_column2
            row_column3 = '<div class="column3">%s</div>' % caption_column3
            row_column4 = '<div class="column4">%s</div>' % caption_column4
            row_column5 = '<div class="column5">%s</div>' % caption_column5
            row_column6 = '<div class="column6">%s</div>' % caption_column6
            row_column7 = '<div class="column7">%s</div>' % caption_column7
            row_column8 = '<div class="column8">%s</div>' % caption_column8
            row_column9 = '<div class="column9">%s</div>' % caption_column9
            row_column10 = '<div class="column10">%s</div>' % caption_column10
            row_column11 = '<div class="column11">%s</div>' % caption_column11
            
            row_clear = '<div style="clear: both;"></div>'            
            
            row_article_xml = '<div class="row-headers"> %s %s %s %s %s %s %s %s %s %s %s %s </div>'  \
                            % (row_column1,row_column2,row_column3,row_column4,row_column5, \
                               row_column6,row_column7,row_column8,row_column9, \
                               row_column10,row_column11,row_clear)
            list += row_article_xml        
            
            #titles are hints
            title_preview = T('Click to preview the article (publish or not)')
            title_edit_title = T('Click to change the title of the article')
            title_edit_content = T('Click to change the content of the article, content is all the body of the article')
            title_edit_extract = T('Click to change the extract of the article, extract is a slice of the content you want to show in search')
            title_delete = T('Click to delete this article')
            title_cats = T('Click to change categories of this article')
            title_keywords = T('Click to change keywords of this article')
            title_edit_name = T('Click to change name of this article')
            title_publish_no = T('Click to hide this article')
            title_publish_yes = T('Click to publish this article')
            title_page_no = T('Click if you want to make this article a page')
            title_page_yes = T('Click if you want to make this article a post')
            title_url_no = T('Click and fill empty to make this a normal article')
            title_url_yes = T('Click if you want to make this article a link to a site, to list in panels need to be a page also')   
    
            icon_edit = IMG(_src=URL(request.application,'static','images/edit.png'), \
                            _alt="edit")
            icon_preview = IMG(_src=URL(request.application,'static','images/preview.png'), \
                               _alt="preview", _style="float:left; padding-left: 4px;")
            icon_remove = IMG(_src=URL(request.application,'static','images/remove.png'), \
                              _alt="remove", _style="float:left;")
                    
            for post in last_posts:                                               
                if post.published==0:                 
                    link_ispublish = A(T("NO"), _href='javascript: void(0);', \
                                       _onclick="ArticlePublish(%s,1);"%(post.id), \
                                       _title="%s"%title_publish_yes)
                else:                 
                    link_ispublish = A(T("YES"), _href='javascript: void(0);', \
                                       _onclick="ArticlePublish(%s,0);"%(post.id), \
                                       _title="%s"%title_publish_no)
                    
                if post.is_page==0:                
                    link_ispage = A(T("NO"), _href='javascript: void(0);', \
                                    _onclick="ArticleAsPage(%s,1);"%(post.id), \
                                    _title="%s"%title_page_no)
                else:                                 
                    link_ispage = A(T("YES"), _href='javascript: void(0);', \
                                    _onclick="ArticleAsPage(%s,0);"%(post.id), \
                                    _title="%s"%title_page_yes)
                
                if post.post_url != "":            
                    link_changeurl = A(T('YES'), _href='javascript: void(0);', \
                                       _onclick="ArticleChangeUrl(%s);"%(post.id), \
                                       _title="%s"%title_url_no)
                else:
                    link_changeurl = A(T('NO'), _href='javascript: void(0);', \
                                       _onclick="ArticleChangeUrl(%s);"%(post.id), \
                                       _title="%s"%title_url_yes)
                
                
                post_title = post.title[:50] #we trunk the size            
                link_preview = A(icon_preview, _href='javascript: void(0);', \
                                 _onclick="ArticlePreview(%s);"%(post.id), \
                                 _title="%s"%title_preview)
                link_title = A(post_title, _href='javascript: void(0);', \
                               _onclick="ArticleChangeTitle(%s);"%(post.id), \
                               _title="%s"%title_edit_title)
                link_content = A(icon_edit, _href='javascript: void(0);', \
                                 _onclick="ArticleChangeContent(%s);"%(post.id), \
                                 _title="%s"%title_edit_content)
                link_extract = A(icon_edit, _href='javascript: void(0);', \
                                 _onclick="ArticleChangeExtract(%s);"%(post.id), \
                                 _title="%s"%title_edit_extract)            
                link_delete = A(icon_remove, _href='javascript: void(0);', \
                                _onclick="ArticleDelete(%s);"%(post.id), \
                                _title="%s"%title_delete)
                link_cat = A(icon_edit, _href='javascript: void(0);', \
                             _onclick="ArticleChangeCategory(%s);"%(post.id), \
                             _title="%s"%title_cats)
                link_changename = A(icon_edit, _href='javascript: void(0);', \
                                    _onclick="ArticleChangeName(%s);"%(post.id), \
                                    _title="%s"%title_edit_name)
                link_Keywords = A(icon_edit, _href='javascript: void(0);', \
                                  _onclick="ArticleChangeKeywords(%s);"%(post.id), \
                                  _title="%s"%title_keywords)
                            
                last_updated = post.updated_on.strftime("%Y-%m-%d:%I:%M:%p")
                                        
                row_column1 = '<div class="column1">%s</div>' % link_title.xml()
                row_column2 = '<div class="column2">%s</div>' % link_content.xml()
                row_column3 = '<div class="column3">%s</div>' % link_extract.xml()
                row_column4 = '<div id="colcat-%s" class="column4">%s</div>' \
                                % (post.id, link_cat.xml())
                row_column5 = '<div class="column5">%s</div>' % link_Keywords.xml()            
                row_column6 = '<div class="column6">%s</div>' % link_ispublish.xml()
                row_column7 = '<div class="column7">%s</div>' % link_ispage.xml()
                row_column8 = '<div class="column8">%s</div>' % link_changeurl.xml()
                row_column9 = '<div class="column9">%s</div>' % link_changename.xml()
                row_column10 = '<div class="column10">%s %s</div>' \
                                % (link_delete.xml(), link_preview.xml())
                row_column11 = '<div class="column11">%s</div>' % last_updated
                
                row_clear = '<div style="clear: both;"></div>'            
                
                row_article_xml = '<div class="row-articles" id="row-%s"> %s %s %s %s %s %s %s %s %s %s %s %s </div>' \
                                    % (post.id,row_column1,row_column2,row_column3, \
                                       row_column4,row_column5,row_column6,row_column7, \
                                       row_column8,row_column9,row_column10,row_column11,row_clear)
                list += row_article_xml
                
            
            if count_posts>max_posts:
                total_pages = count_posts // max_posts
                if (count_posts % max_posts)>0:
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
                             _onclick="ArticleList(%s,'%s');"%(currentpage-1, search_text))           
                forward = A(T("Next"), _href='javascript: void(0);', \
                            _onclick="ArticleList(%s,'%s');"%(currentpage+1,search_text))
                            
                listpages=""    
                if currentpage>1:
                    listpages += "<li>%s</li>" % backward.xml()                             
                
                for page in range(first_page, last_page+1):                
                    page_a = A(unicode(page), _href='javascript: void(0);', \
                               _onclick="ArticleList(%s,'%s');"%(page,search_text))
                    
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
            page_content=list + "%s"%T("No articles")   
        
        html_content = '<h2>%s</h2>'%T("Articles")
        html_content += '%s'%page_content
        info={}          
        info['html']=sanitate_string(html_content)                 
        
        return sj.dumps(info)                    



    def add(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        session = self.i2p.environment.session
        
        if request.env.web2py_runtime_gae: #in gae only the admin can fill articles, with id=0
            user_id = 0
        else: 
            user_id = session.auth.user.id #extract user id
        
        no_title = sanitate_string("%s"%T('No Title'))
        no_description = sanitate_string("%s"%T('No description'))
                    
        idpost = db.posts.insert(title = no_title,
                                 description = no_description,
                                 text_slice = no_description,                                                          
                                 created_by_id = user_id,
                                 updated_by_id = user_id,
                                 published = 0,
                                 is_page = 0)
        
        if idpost>0:        
            return json_response(message= T("Article added"),\
                                 alert=0,value="")
        else:
            return json_response(message=T("The article id doesn't exist"),\
                                 alert=2,value="")
    
    
    def delete(self, id):  
        
        db = self.i2p.db
        T = self.i2p.environment.T
              
        posts = db(db.posts.id == id).select()
        if posts:
            post = posts[0]
            id_post = post.id
            db(db.comments.post_id == id_post).delete()        
            db(db.posts.id == id_post).delete()        
            return json_response(message=T("Article deleted"),\
                                 alert=0,value="")      
        else:
            return json_response(message=T("The article id doesn't exist"),\
                                 alert=2,value="")   


    def change_title(self, id, value): 
        
        db = self.i2p.db
        T = self.i2p.environment.T
        fulltext_field = self.i2p.config.fulltext_field
                   
        flat_name = (IS_SLUG()(value))[0]     
        count = db((db.posts.name == flat_name)&(db.posts.id != id)).count()
        if count>0: #if not exist the name in post db, then ok i assign the name flated
            name=""
        else:
            name=flat_name
               
        posts = db(db.posts.id == id).select()
        if posts:
            post = posts[0]        
            list_keys = post.keywords #get keywords
            keyswords = self._keywords_as_string(list_keys)    
            clean_words = self._make_searchable(value, keyswords, post.description)   
                                             
            if fulltext_field == 'full_text': #horrible
                post.update_record(title = value, name = name, full_text = clean_words)                
            else:                                             
                post.update_record(title = value, name = name, fulltext = clean_words)
                        
            return json_response(message=T("Title changed"),\
                                 alert=0,value="")      
        else:
            return json_response(message=T("The article id doesn't exist"),\
                                 alert=2,value="")   
        
    
    
    def get_title(self, id):  
        
        db = self.i2p.db
        T = self.i2p.environment.T
           
        posts = db(db.posts.id == id).select()
        if posts:
            post = posts[0]
            value = post.title       
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message=T("The article id doesn't exist"),\
                                 alert=2,value="")
   


    def change_content(self, id, value):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        fulltext_field = self.i2p.config.fulltext_field
                
        #if self.i2p.config.editor_language in ['Markmin']:
        #    value = clean_html(value) #in markmin I have to clean tags
                
        posts = db(db.posts.id == id).select()
        if posts:
            post = posts[0]         
            list_keys = post.keywords #get keywords                        
            keyswords = self._keywords_as_string(list_keys)                                          
            clean_words = self._make_searchable(post.title, keyswords, value)                                         
            updated_on = datetime.datetime.today() 
             
            if fulltext_field == 'full_text': #horrible                                
                post.update_record(description = value, full_text = clean_words, updated_on=updated_on)                
            else:             
                post.update_record(description = value, fulltext = clean_words, updated_on=updated_on)  
                
                 
            return json_response(message=T("Content changed"),\
                                 alert=0,value="")        
        else:
            return json_response(message=T("The article id doesn't exist"),\
                                 alert=2,value="")  
            
            
    def _make_searchable(self, title="", keywords="", content=""): 
        
        config = self.i2p.config
        request = self.i2p.environment.request
                            
        if request.env.web2py_runtime_gae:
            searchable = " %s %s %s " % (sanitate_string(title,'ignore'), \
                                     sanitate_string(keywords,'ignore'), \
                                     sanitate_string(content,'ignore'))
            clean_words = get_clean_words_gae(searchable,config.language)
        else:
            searchable = " %s %s %s " % (title, \
                                     keywords, \
                                     content)                                
            clean_words = get_clean_words(searchable,config.language)
        
        return clean_words  


    def get_content(self, id):
        
        db = self.i2p.db
        T = self.i2p.environment.T
            
        posts = db(db.posts.id == id).select()
        if posts:
            post = posts[0]
            value = post.description
            return json_response(message="",alert=0,value=value)        
        else:
            return json_response(message=T("The article id doesn't exist"),\
                                 alert=2,value="")   
        
        
    def change_extract(self, id, value):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        #if self.i2p.config.editor_language in ['Markmin']:
        #    value = clean_html(value) #in markmin I have to clean tags
                
        posts = db(db.posts.id == id).select()
        if posts:
            post = posts[0]        
            post.update_record(text_slice = value)        
            return json_response(message= T("Extract changed"),\
                                 alert=0,value="")        
        else:
            return json_response(message=T("The article id doesn't exist"),\
                                 alert=2,value="")  
        
        
    def get_extract(self, id):
        
        db = self.i2p.db
        T = self.i2p.environment.T   
     
        posts = db(db.posts.id == id).select()
        if posts:
            post = posts[0]
            value = post.text_slice        
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message=T("The article id doesn't exist"),\
                                 alert=2,value="") 
        
    
    def _keywords_to_proper_list(self, value):
        
        db = self.i2p.db
        request = self.i2p.environment.request
                
        keywordsList=[]
        keywords = value.split(',')#first separate the keys
        for keyw in keywords:
            cleanKeyword = keyw.strip()            
            if request.env.web2py_runtime_gae:
                cleanKeyword = normalize_word(cleanKeyword)
            else:           
                cleanKeyword = cleanKeyword.lower()#lower the words
                                
            if cleanKeyword=="":
                continue            
            keywordsList.append(cleanKeyword)
            
        keywordsList = {}.fromkeys(keywordsList).keys() # Remove duplicate
        try: keywordsList.remove('') 
        except: pass #remove 
        
        return keywordsList
    
    
    def _keywords_as_string(self,keywordsList):
        
        if keywordsList:               
            keyswordsTxt = " ".join(keywordsList) #transform to string
        else:
            keyswordsTxt = ""
        
        return keyswordsTxt 
 
       
    def change_keywords(self, id, value):
        
        db = self.i2p.db
        T = self.i2p.environment.T 
        admin_tags =  self.i2p.admin_tags
        fulltext_field = self.i2p.config.fulltext_field
                        
        posts = db(db.posts.id == id).select()
        if posts:
            post = posts[0]        
            keywordsList = self._keywords_to_proper_list(value)        
            try:
                                
                keyswordsTxt = self._keywords_as_string(keywordsList)                 
                clean_words = self._make_searchable(post.title, keyswordsTxt, post.description)            
                if fulltext_field == 'full_text': #horrible           
                    post.update_record(keywords = keywordsList, full_text = clean_words)
                else:
                    post.update_record(keywords = keywordsList, fulltext = clean_words)
                       
                admin_tags.save_keywords_as_tags(id, keywordsList)
            
            except:                       
                db.rollback()                
                return json_response(message=T("Problem in change keywords"),\
                                     alert=2,value="")        
            else:
                db.commit()           
                return json_response(message=T("Keywords changed"),\
                                     alert=0,value="")     
        else:
            return json_response(message=T("The article id doesn't exist"),\
                                 alert=2,value="")       


    def get_keywords(self, id): 
        
        db = self.i2p.db
        T = self.i2p.environment.T 
           
        posts = db(db.posts.id == id).select()
        if posts:
            post = posts[0]
            list = post.keywords  
            if list:               
                value = ",".join(list) #transform to separeted comma
            else:
                value = ""        
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message=T("The post id doesn't exist"),\
                                 alert=2,value="")   


    def change_name(self, id, value):
        
        db = self.i2p.db
        T = self.i2p.environment.T
                
        posts = db(db.posts.id == id).select()
        if posts:
            post = posts[0]
            name = (IS_SLUG()(value))[0] #_utils_flat_title(value)        
            post.update_record(name = name)        
            return json_response(message=T("The name was changed"),\
                                 alert=0,value="")
        else:        
            return json_response(message=T("The article id doesn't exist"),\
                                 alert=2,value="")        


    def get_name(self, id):
        
        db = self.i2p.db
        T = self.i2p.environment.T
            
        posts = db(db.posts.id == id).select()
        if posts:
            post = posts[0]
            value = post.name        
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message=T("The article id doesn't exist"),\
                                 alert=2,value="")


    def change_status(self, id, value): 
        
        db = self.i2p.db
        T = self.i2p.environment.T
          
        if value!=1:
            value=0         
        posts = db(db.posts.id == id).select()
        if posts:
            post = posts[0]
            published_on = datetime.datetime.today()        
            post.update_record(published = value, published_on=published_on)       
            return json_response(message=T("The status of article was changed"),\
                                 alert=0,value="")     
        else:
            return json_response(message=T("The article id doesn't exist"),\
                                 alert=2,value="")
        
    
    def get_status(self, id):  
        
        db = self.i2p.db
        T = self.i2p.environment.T
         
        posts = db(db.posts.id == id).select()
        if posts:
            post = posts[0]
            value = post.published        
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message=T("The article id doesn't exist"),\
                                 alert=2,value="")
     


    def change_ispage(self, id, value): 
        
        db = self.i2p.db
        T = self.i2p.environment.T
          
        if value!=1:
            value=0         
        posts = db(db.posts.id == id).select()
        if posts:
            post = posts[0]        
            post.update_record(is_page = value)        
            return json_response(message=T("The status of article was changed"),\
                                 alert=0,value="")      
        else:        
            return json_response(message=T("The article id doesn't exist"),\
                                 alert=2,value="") 
                
        
    def get_ispage(self, id):   
        
        db = self.i2p.db
        T = self.i2p.environment.T
         
        posts = db(db.posts.id == id).select()
        if posts:
            post = posts[0]
            value = post.is_page
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message=T("The article id doesn't exist"),\
                                 alert=2,value="")
        

    def change_url(self, id, value):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        value =  value.strip()  
        (url, notvalid) = (IS_URL()(value))
        if notvalid and value!="":
            return json_response(message=T("The url-link is not valid use ex.: http://www.mysite.com or fill with blank to disable this function"),alert=2,value="")
                 
        posts = db(db.posts.id == id).select()
        if posts:
            post = posts[0]        
            post.update_record(post_url = url)        
            return json_response(message= T("Url changed"),\
                                 alert=0,value="")        
        else:
            return json_response(message=T("The article id doesn't exist"),\
                                 alert=2,value="")         
    
    
    def get_url(self, id):   
        
        db = self.i2p.db
        T = self.i2p.environment.T
           
        posts = db(db.posts.id == id).select()
        if posts:
            post = posts[0]
            value = post.text_slice        
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message=T("The article id doesn't exist"),\
                                 alert=2,value="")  


    
    


