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

from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *
import gluon.contrib.simplejson as sj

#local
from utils import *


class Widgets(object): 
    
    def __init__(self, i2p):
        
        self.i2p = i2p        
        
        

    def get_menu(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        config = self.i2p.config
        articles = self.i2p.articles
        
        
        #this list the top pages
        #the maximun display lenght of title is 25 characters
        xml_pages=""
        trunk_title = 25
        (pages, pages_count) = articles.get_last_pages(1)       
        for page in pages:        
            (url, notvalid) = (IS_URL()(page.post_url))
            if notvalid: #this is a normal post               
                link_page = articles.get_page_permanent_link(page.id, \
                                                              page.title[:trunk_title])
            else: #this is a url-post                        
                link_page = A(page.title[:trunk_title], _href=page.post_url)          
            xml_page = '<li>%s</li>' % link_page.xml()                      
            #xml_pages += sanitate_string(xml_page)
            xml_pages += xml_page
            
        link_home = A(T('Home'), _href=URL(request.application,\
                                           config.controller_default,\
                                           'index'))
        xml_menu='<ul><li>%s</li> %s </ul>' % (link_home,xml_pages)   
            
        return xml_menu          
        
      
      

    def front(self):
        
        config = self.i2p.config
        siteinfo = self.i2p.siteinfo
            
        if config.front_enabled:   
            welcome_description = '<div class="entry">%s</div>' \
                                    % siteinfo._get_frontpage()
            xml = '<div class="post"> %s </div>' % welcome_description    
        else:
            xml=""
            
        return xml
    
        

    def sidebar_aboutme(self): 
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        config = self.i2p.config
        siteinfo = self.i2p.siteinfo
        
        about_xml = ""
        if config.about_enabled:   
            about_caption = T('About')
            about_info = siteinfo._get_aboutme()
            if about_info != "":
                about_description = '%s' % about_info
                about_xml = '<div id="sidebar-about"><h2>%s</h2> %s </div>' \
                                % (about_caption, about_description)
        
        return about_xml 
      


    def sidebar_archive(self):        
        
        config = self.i2p.config
        articles = self.i2p.articles
        
        archive_xml = ""
        if config.archive_enabled:
            archive_generate=""
            if not config.widgets_ajax:        
                archive_generate = articles.get_list_archives()                    
            archive_xml = '<div id="sidebar-archive"> %s </div>' % archive_generate
                
        return archive_xml
    
    

    def footer_archive(self):
        
        config = self.i2p.config
        articles = self.i2p.articles
        
        archive_xml = ""
        if config.archive_enabled:
            archive_generate=""
            if not config.widgets_ajax:        
                archive_generate = articles.get_list_archives()                    
            archive_xml = '<div id="footer-widgets-archives" class="footer-columns"> %s </div>' \
                            % archive_generate
                
        return archive_xml



    def get_pages(self):
        
        T = self.i2p.environment.T
            
        pages_caption = T('Pages')
        pages_generate = self.get_menu()
        xml_pages = '<h2>%s</h2> %s' % (pages_caption,pages_generate)
        return xml_pages



    def sidebar_pages(self):
        
        config = self.i2p.config
        
        pages_xml = ""
        if config.pages_enabled:
            pages_generate=""
            if not config.widgets_ajax:
                pages_generate = self.get_pages()                      
                        
            pages_xml = '<div id="sidebar-pages"> %s </div>' % (pages_generate)
                
        return pages_xml



    def footer_pages(self):
        
        config = self.i2p.config
        
        pages_xml = ""
        if config.pages_enabled:
            pages_generate=""
            if not config.widgets_ajax:
                pages_generate = self.get_pages()                      
                        
            pages_xml = '<div id="footer-widgets-pages" class="footer-columns"> %s </div>' \
                            % (pages_generate)
                
        return pages_xml
    
    

    def sidebar_links(self):
        
        config = self.i2p.config
        articles = self.i2p.articles
        
        links_xml = ""
        if config.pages_enabled:
            links_generate=""
            if not config.widgets_ajax:
                links_generate = articles.get_list_links()                      
                        
            links_xml = '<div id="sidebar-links"> %s </div>' % (links_generate)
                
        return links_xml
    
    

    def load_last_comments(self, page=1):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        xml_comments=""
        last_comments=""
        header = T('Last comments')
        (limit_inf, limit_sup) = get_query_limits(page, 5) #the last five comments
        query = (db.comments.id>0)    
        last_comments = db(query).select(db.comments.ALL,\
                                         orderby=~db.comments.comment_on,\
                                         limitby=(limit_inf, limit_sup))
        for comment in last_comments: 
            #author_avatar = IMG(_src=URL(r=request,c='static',f='images/avatar.png'), alt="avatar", style="padding: 5px; float:left;")
            author_sytle = ""#"padding: 5px; float:left;"
            author_avatar = self.i2p.comments._get_avatar(comment.author_id,\
                                                          style=author_sytle)
            text_comment = comment.comment[:60]
            comment_user = self.i2p.users.get_user_title(comment.author_id)
            comment_time = comment.comment_on.strftime("%B %d, %Y:%I:%M %p")
            link_post = self.i2p.articles.get_post_permanent_link(comment.post_id)  
            xml_comment = '<li><div style="float:left">%s</div> %s say: %s on %s on article %s</li>' \
                            % (author_avatar.xml(), comment_user, text_comment, \
                               comment_time, link_post.xml())        
            #xml_comments += sanitate_string(xml_comment)
            xml_comments += xml_comment
        
        if xml_comments!="":
            last_comments="<h2>%s</h2><ul>%s</ul>" % (header,xml_comments)
            
        return last_comments
    
    
    

    def sidebar_last_comments(self):
        
        
        comments_xml = ""
        config = self.i2p.config
        
        if config.comments_method in ['Disqus']:
            comments_xml = '<div id="sidebar-last-comments"> %s </div>' % self._disqus_last_comments()
            
        elif config.comments_method in ['Enabled']:
            comments_generate=""
            if not config.widgets_ajax:
                comments_generate = self.load_last_comments()                      
                        
            comments_xml = '<div id="sidebar-last-comments"> %s </div>' % (comments_generate)
                
        return comments_xml



    def sidebar_tags(self):
        
        config = self.i2p.config
        articles = self.i2p.articles
        
        tags_xml = ""
        if config.tags_enabled:
            tags_generate=""
            if not config.widgets_ajax:
                tags_generate = articles.get_popular_tags()                    
            tags_xml = '<div id="sidebar-tags">%s</div><div style="clear: both; float: none;"></div>' \
                        % tags_generate
            
        return tags_xml



    def sidebar_feed(self): 
        
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        config = self.i2p.config
        
        feed_xml = ""
        if config.feed_enabled:   
            feed_caption = T('Rss')
            icon_feed_url = URL(request.application,'static','images/feed.png')  
            img_feed = IMG(_src=icon_feed_url, _alt="Feed", _style="padding-left: 5px;")       
            link_feedposts = A(T("Rss last posts"), \
                               _href=URL(request.application,\
                                         config.controller_default,\
                                         'feed_articles.rss' ))
            link_feedcomments = A(T("Rss last comments"), \
                                  _href=URL(request.application,\
                                            config.controller_default,\
                                            'feed_comments.rss' ))
            feed_posts = '<li>%s %s</li>' % (link_feedposts, img_feed.xml())
            feed_comments = '<li>%s %s</li>' % (link_feedcomments, img_feed.xml())
            feed_xml = '<div id="sidebar-feed"><h2>%s</h2> <ul> %s %s </ul> </div>' \
                        % (feed_caption, feed_posts, feed_comments)
        
        return feed_xml 
    
    

    def load_last_posts(self):
        
        articles = self.i2p.articles
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        xml_posts=""
        last_posts=""
        last_entries = T('Last entries')
        (posts, post_count) = articles.get_last_posts(1)                  
        for post in posts:            
            link_post = articles.get_post_permanent_link(post.id, \
                                                          post.title)  
            xml_post = '<li>%s</li>' % link_post.xml()        
            xml_posts += xml_post
        
        if xml_posts!="":
            last_posts="<h2>%s</h2><ul>%s</ul>" % (last_entries,xml_posts)
            
        return last_posts
    
    
    

    def sidebar_last_posts(self):
        
        config = self.i2p.config    
        last_posts=''
        
        if config.last_post_enabled:
            xml_posts=""
            if not config.widgets_ajax:
                xml_posts = self.load_last_posts()  
            last_posts='<div id="sidebar-last-posts">%s</div>' % xml_posts
           
        return last_posts 
    



    def footer_last_posts(self):
        
        config = self.i2p.config
            
        last_posts=''
        if config.last_post_enabled:
            xml_posts=""
            if not config.widgets_ajax:
                xml_posts = self.load_last_posts()  
            last_posts='<div id="footer-widgets-last-posts" class="footer-columns">%s</div>' \
                        % xml_posts
           
        return last_posts



    def load_categories(self):
        
        config = self.i2p.config
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
         
        xml_cats=""
        categories=""
        cats = self.i2p.categories.get_list(page=1, limit=30)       
        for cat in cats:
            post_count = db(db.posts.categories.contains(str(cat.id))).count() #contains bug in web2py              
            text_cat = " %s (%s)" % (cat.title,post_count)
            link_cat = A(text_cat,_title="%s"%cat.description,\
                         _href=URL(request.application,\
                                   config.controller_default,\
                                   'category/by_id', args=[unicode(cat.id)] ))                     
            xml_cat = '<li>%s</li>' % link_cat.xml()            
            xml_cats += xml_cat        
        if xml_cats!="":            
            categories = "<h2>%s</h2>"%T('Categories')
            categories += "<ul>%s</ul>"%xml_cats                
            
        return categories  
    
    

    def sidebar_categories(self):
        
        config = self.i2p.config
            
        xml_categories = ""
        if config.categories_enabled:
            xml_cats=""
            if not config.widgets_ajax:
                xml_cats = self.load_categories()  
                        
            xml_categories='<div id="sidebar-categories">%s</div>' % xml_cats
                        
        return xml_categories
    
        

    def footer_categories(self):
        
        config = self.i2p.config
            
        xml_categories = ""
        if config.categories_enabled:
            xml_cats=""
            if not config.widgets_ajax:
                xml_cats = self.load_categories()  
                        
            xml_categories='<div id="footer-widgets-categories" class="footer-columns">%s</div>' \
                            % xml_cats
                        
        return xml_categories
    
    
        

    def sidebar_search(self):
        
        config = self.i2p.config
        T = self.i2p.environment.T
        request = self.i2p.environment.request
         
        xml_content = ""
        if config.search_enabled:   
            title_search = T('Search')
            search_url = URL(request.application, \
                             config.controller_default,\
                             'search')    
            xml_content = '''<div id="sidebar-search" >
                            <h2>%s</h2>
                            <form method="get" action="%s">                                       
                            <div><input type="text" name="q" id="sidebar-search-text" value="" /></div>
                            <div><input type="submit" id="sidebar-search-submit" value="Search" /></div>                                       
                            </form>
                            </div>
                            
                                ''' % (title_search,search_url)
        return xml_content 
    
    


    def add_this(self, url="",title="",description=""):
        
        config = self.i2p.config        
        
        #need fix: need to escape to somethin like: &amp;
        if title!='':        
            addthis_title = 'addthis:title="%s"' % clean_html(title)
        else:
            addthis_title = ''
            
        if url!='':
            addthis_url = 'addthis:url="%s"' % url
        else:
            addthis_url = ''
            
        if description!='':
            addthis_description = 'addthis:description="%s"' % clean_html(description)
        else:
            addthis_description = ''
        
        addthis = '''<!-- AddThis Button BEGIN -->
        <div class="addthis_toolbox addthis_default_style">
        <a href="http://www.addthis.com/bookmark.php?v=250&amp;username=%(username)s" class="addthis_button_compact" %(url)s %(title)s %(description)s >Share</a>
        <span class="addthis_separator">|</span>
        <a class="addthis_button_facebook" %(url)s %(title)s %(description)s></a>
        <a class="addthis_button_myspace" %(url)s %(title)s %(description)s></a>
        <a class="addthis_button_google" %(url)s %(title)s %(description)s></a>
        <a class="addthis_button_twitter" %(url)s %(title)s %(description)s></a>
        </div>
        <script type="text/javascript" src="http://s7.addthis.com/js/250/addthis_widget.js#username=%(username)s"></script>
        <!-- AddThis Button END --> ''' % {'username': config.addthis_user, 'url': addthis_url, 'title': addthis_title, 'description': addthis_description}
        return addthis




    def post_meta(self, post):
                
        
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        config = self.i2p.config
        articles = self.i2p.articles
        users = self.i2p.users
        
        
        post_author_caption = '<span class="author">%s</span>' \
                                % users.get_user_title(post.created_by_id)    
        post_category = articles.get_post_category(post.id)
        
        if post_category=="":
            post_category = T("uncategorized")
            in_category = T('in')
        else:
            in_category = T('in categories')
            
        #post_time = post.published_on.strftime("%B %d, %Y at %I:%M")
        post_time = post.published_on.strftime("%Y-%m-%d %I:%M")
        year_full = post.published_on.strftime("%Y")    
        month = post.published_on.strftime("%m")
        link_time = A(post_time, _href=URL(request.application,\
                                           config.controller_default,\
                                           'archives',args=[year_full,month]))
        posted_by = T('By')
          
        updated_on = T('Published on')       
        byline = '%s %s %s %s %s %s' % (updated_on, link_time.xml(), posted_by, \
                                        post_author_caption, in_category, post_category)
        
        return byline




    def post_extract(self, post):
        
        config = self.i2p.config
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        comments = self.i2p.comments
        articles = self.i2p.articles
        
        
        label_comments = "%s" % T('Comments')
        if config.comments_method in ['Enabled'] and not config.widgets_ajax:
            comments_count = comments._get_comment_count(post.id)  
        elif config.comments_method in ['Disqus']:
            comments_count = ""
        else:
            comments_count = 0
        
        if config.comments_method in ['Disqus']:
            link_comments = articles.get_post_permanent_link(post.id, \
                                                                      'Comments', \
                                                                      'disqus_thread')
        else:          
            link_comments = articles.get_post_permanent_link(post.id, \
                                                                      label_comments, \
                                                                      'comments')  
              
        link_readmore = articles.get_post_permanent_link(post.id, T("Read more"))
        base_http = 'http://' + str(request.env.http_host)
        url_permanent = articles.get_post_permanent_link(post.id, only_url=True )
        url_post = str(base_http + url_permanent)
        
        if config.addthis_enabled:
            #add_this = self.add_this(url_post,post.title,post.text_slice[:100]) #need to pass: title, url, description             
            add_this = self.add_this(url_permanent,post.title,post.text_slice[:100]) #need to pass: title, url, description
        else:
            add_this = ""
                   
        xml_post = '<div class="post">'
        xml_post +='<h2 class="title">%s</h2>' \
                    % articles.get_post_permanent_link(post.id).xml()
        xml_post +='''<div class="meta">%s  - 
                        <span class="comments-count" id="comments-count_%s"> %s </span>
                        %s 
                         </div>''' \
                         % (self.post_meta(post), post.id, comments_count, link_comments.xml()) 
        
        if config.editor_language in ['Markmin']:
            text_slice = MARKMIN(post.text_slice)
        else:
            text_slice = post.text_slice 
                     
        xml_post +='<div class="entry">%s</div>' % text_slice                
        xml_post +='''<div class="links">
                        <div class="readmore"> %s </div>                          
                        <div class="addthis"> %s </div>
                        <div style="float:none; clear:both;"></div>                        
                    </div>''' % (link_readmore.xml(), add_this)  
        xml_post +='</div>'
        
        return xml_post
    



    def last_posts(self, page):
        
        articles = self.i2p.articles       
        (posts, count_posts) = articles.get_last_posts(page)       
        xml_posts = articles.get_xml_results_from_posts(posts)
        xml_posts += articles.pagination_last_post(page, count_posts)        
        return xml_posts



    def disqus_comments(self):
        
        config = self.i2p.config
        
        if config.disqus_dev:
            developer = 'var disqus_developer = 1;';
        else:
            developer = '';
            
        script = '''
        <div id="disqus_thread"></div>
        <script type="text/javascript">
        %(developer)s
          /**
            * var disqus_identifier; [Optional but recommended: Define a unique identifier (e.g. post id or slug) for this thread] 
            */
          (function() {
           var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
           dsq.src = 'http://%(site)s.disqus.com/embed.js';
           (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
          })();
        </script>
        <noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript=%(site)s">comments powered by Disqus.</a></noscript>
        <a href="http://disqus.com" class="dsq-brlink">blog comments powered by <span class="logo-disqus">Disqus</span></a>
    
         ''' % {'developer': developer, 'site': config.disqus_site}
        return script
    
    
    

    def disqus_comments_count(self):
        
        config = self.i2p.config
        
        script = ''' 
        <script type="text/javascript">
        var disqus_shortname = '%(site)s';
        (function () {
          var s = document.createElement('script'); s.async = true;
          s.src = 'http://disqus.com/forums/%(site)s/count.js';
          (document.getElementsByTagName('HEAD')[0] || document.getElementsByTagName('BODY')[0]).appendChild(s);
        }());
        </script>
        ''' % {'site': config.disqus_site}
        
        
        return script
    



    def _disqus_last_comments(self):
        
        T = self.i2p.environment.T
        config = self.i2p.config
        
        if self.i2p.config.avatars_enabled:
            hide_avatars = 0
        else:
            hide_avatars = 1
            
        avatar_size = self.i2p.config.avatar_size
        recent_comments=T("Recent Comments")
        num_items = 5
        
        script = '''
        <div id="recentcomments" class="dsq-widget">
        <h2 class="dsq-widget-title">%(recent_comments)s</h2>
        <script type="text/javascript" src="http://disqus.com/forums/%(site)s/recent_comments_widget.js?num_items=%(num_items)s&hide_avatars=%(hide_avatars)s&avatar_size=%(avatar_size)s&excerpt_length=200">
        </script>
        </div>
        <a href="http://disqus.com/">Powered by Disqus</a>
        '''  % {'site': config.disqus_site, 'recent_comments': recent_comments, 'avatar_size': avatar_size, 'hide_avatars': hide_avatars, 'num_items': num_items}
        
        return script
    
    
    
    def sidebar_popular_threads(self): 
        
        config = self.i2p.config    
        popular_threads=''
        
        #for now only in disqus
        if config.comments_method in ['Disqus']:                          
            popular_threads='<div id="sidebar-popular-threads">%s</div>' % self._disqus_popular_threads()
           
        return popular_threads  

    
    
    
    def _disqus_popular_threads(self):
        
        config = self.i2p.config
        T = self.i2p.environment.T
        popular_threads=T("Popular Threads")
        script = '''
        <div id="popularthreads" class="dsq-widget">
        <h2 class="dsq-widget-title">%(popular_threads)s</h2>
        <script type="text/javascript" src="http://disqus.com/forums/%(site)s/popular_threads_widget.js?num_items=5">
        </script>
        </div>
        <a href="http://disqus.com/">Powered by Disqus</a>
        '''% {'site': config.disqus_site,'popular_threads':popular_threads}
        
        return script




    def sidebar_top_commenters(self): 
        
        config = self.i2p.config    
        top_commenters=''
        
        #for now only in disqus
        if config.comments_method in ['Disqus']:                          
            top_commenters='<div id="sidebar-top-commenters">%s</div>' % self._disqus_top_commenters()
           
        return top_commenters  

    
    
    
    def _disqus_top_commenters(self):
        
        T = self.i2p.environment.T
        config = self.i2p.config
        avatar_size = self.i2p.config.avatar_size
        
        if self.i2p.config.avatars_enabled:
            hide_avatars = 0
        else:
            hide_avatars = 1
            
        num_items = 5
            
        
        top_commenters=T('Top Commenters')
        script = '''        
        <div id="topcommenters" class="dsq-widget">
        <h2 class="dsq-widget-title">%(top_commenters)s</h2>
        <script type="text/javascript" src="http://disqus.com/forums/%(site)s/top_commenters_widget.js?num_items=%(num_items)s&hide_mods=0&hide_avatars=%(hide_avatars)s&avatar_size=%(avatar_size)s">
        </script>
        </div>
        <a href="http://disqus.com/">Powered by Disqus</a>       
        '''% {'site': config.disqus_site, 'top_commenters':top_commenters, 'avatar_size':avatar_size, 'hide_avatars':hide_avatars, 'num_items':num_items}
        
        return script
    
    
    
    def sidebar_combination(self): 
        
        config = self.i2p.config  
        T = self.i2p.environment.T  
        head_combination = T('Posts')
        combination=''
        
        #for now only in disqus
        if config.comments_method in ['Disqus']:                          
            combination='<div id="sidebar-combination"><h2>%s</h2>%s</div>' % (head_combination, self._disqus_combination())
           
        return combination
    
    
    
    
    def _disqus_combination(self):
        
        config = self.i2p.config
        num_items = 5
        script = '''
        <script type="text/javascript" src="http://disqus.com/forums/%(site)s/combination_widget.js?num_items=%(num_items)s&hide_mods=0&color=grey&default_tab=recent&excerpt_length=200">
        </script>
        <a href="http://disqus.com/">Powered by Disqus</a>
        '''% {'site': config.disqus_site, 'num_items':num_items}
        
        return script




    def ga_script(self):
        
        config = self.i2p.config
        script=""
        if config.ga_enabled:
            script = ''' 
                <script>
               var _gaq = [['_setAccount', '%(ga_id)s'], ['_trackPageview']];
               (function(d, t) {
                var g = d.createElement(t),
                    s = d.getElementsByTagName(t)[0];
                g.async = true;
                g.src = '//www.google-analytics.com/ga.js';
                s.parentNode.insertBefore(g, s);
               })(document, 'script');
              </script>
            ''' % {'ga_id': config.ga_id}      
        
        
        return script


