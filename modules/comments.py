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

ADMIN_MAX_LIST_PAGES = 10
COMMENTS_LIST_PER_PAGE = 5
ADMIN_COMMENTS_LIST_PER_PAGE = 5

class Comments(object): 
    
    
    def __init__(self, i2p):
        
        self.i2p = i2p        
               
        
    def define_tables(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        db.define_table('comments',                                  
            Field('id', 'id'),
            Field('post_id', 'integer', required=True), 
            Field('author_id', 'integer', required=True),
            Field('author_name', 'string', length=255, default=""), #not used, perhaps in a future,
                                                                    #anonymous comment?
            Field('author_email', 'string', length=255, default=""), #not used, perhaps in a future,
                                                                     #  anonymous comment?
            Field('author_url', 'text', default=""), #not used, perhaps in a future anonymous comment?
            Field('reply_id', 'integer', default=0, required=True),
            Field('approved', 'integer', default=0), #not used now, future: approved comment?                                    
            Field('comment', 'text', default="", required=True),
            Field('comment_on', 'datetime', default=datetime.datetime.today()),                                                                                                            
            migrate=self.i2p.config.is_first_time)
        
        db.comments.comment.requires = IS_NOT_EMPTY()
        db.comments.post_id.requires = IS_IN_DB(db, 'posts.id', 'posts.title')
        db.comments.author_id.requires = IS_IN_DB(db, 'auth_user.id', 'auth_user.email')
        
        
    def _count(self, id_post):
        
        db = self.i2p.db
        T = self.i2p.environment.T
            
        comment_count = db(db.comments.post_id==id_post).count()
        return comment_count   


    def count(self, id_post): 
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        if self.i2p.config.comments_method in ['Enabled']:       
            count = self._count(id_post)
        else:
            count = 0
            
        info={}          
        info['count']=count        
        return sj.dumps(info)



    def _get_all(self, id_post, page): #get_comments_from_post
        
        db = self.i2p.db
        T = self.i2p.environment.T
            
        (limit_inf, limit_sup) = get_query_limits(page, COMMENTS_LIST_PER_PAGE)    
        query = (db.comments.post_id==id_post)
        comments_count = db(query).count()
        comments = db(query).select(db.comments.ALL, \
                                    orderby=~db.comments.comment_on, \
                                    limitby=(limit_inf, limit_sup))   
            
        return (comments, comments_count)



    def generate_title(self, id): #_comments_title_from_post  
        
        
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        if not self.i2p.config.comments_method in ['Enabled']:
            return json_response(message=T('The comments are disabled'),\
                                 success=0,alert=2)
          
        comments_count = self._get_all(id, 1)[1]    
        if comments_count == 0:
            text_response = T('No Responses')
        elif comments_count == 1:
            text_response = T('Response')
        elif comments_count > 1:
            text_response = T('Responses')
        
        title_post = self.i2p.articles.get_post_permanent_link(id)
        title_comment = '<h2>%s to &#8220 %s &#8221;</h2>' % (text_response, title_post)
        
        info={}
        info['html']=title_comment        
        return sj.dumps(info)



    def generate_reply(self, id): #_comments_form_from_post
        
        auth = self.i2p.environment.auth
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        if not self.i2p.config.comments_method in ['Enabled']:
            return json_response(message=T('The comments are disabled'),\
                                 success=0,alert=2)
        
        xml_form=""
        reply_id = 0
        no_comments = T('You can reply leaving your comment.')
        login_link = A(T("Sign in"), \
                       _href=URL(request.application, \
                                 self.i2p.config.controller_default, \
                                 'user/login'))    
        need_register = T('You have to %s to your account before comment.') \
                        % login_link.xml()
        if not 'register' in auth.settings.actions_disabled:
            register_link = A(T("Register"), \
                              _href=URL(request.application, \
                                        self.i2p.config.controller_default, \
                                        'user/register'))
            register_action = T("If you don't have an account you can %s one.") \
                                % register_link.xml()
        else:
            register_action = T("Register is disabled.")
            
        if self.i2p.users.is_user_logged_in():                    
            xml_form += '<div class="comment" id="comment-%s">%s</div>' \
                            % (reply_id, no_comments)
            new_form = '''<script type="text/javascript" charset="utf-8">
                        jQuery(document).ready(function(){ ShowReplyBox(%s,%s);  });
                        </script>''' %(id,0)
            xml_form += new_form            
        else:
            xml_form += '<div class="comment" id="comment-%s">%s %s %s</div>' \
                        % (reply_id, no_comments, need_register, register_action)
            
        info={}
        info['html']=xml_form        
        return sj.dumps(info)
    
    

    def get_all(self, id, page, isadmin=False): #_comments_from_post
        
        T = self.i2p.environment.T
        request = self.i2p.environment.request  
        
        if not self.i2p.config.comments_method in ['Enabled']:
            return json_response(message=T('The comments are disabled'),\
                                 success=0,alert=2)
           
        max_list_per_page=COMMENTS_LIST_PER_PAGE       
        (comments, comments_count) = self._get_all(id, page)     
        list_comments =''
        reply_id = 0    
        inc=0    
        for comment in comments:
            comment_user = self.i2p.users.get_user_title(comment.author_id)
            comment_time = comment.comment_on.strftime("%B %d, %Y at %I:%M %p")
            if isadmin:
                admin_edit = (A(T("Edit"), _href='javascript: void(0);', \
                                _onclick="CommentEdit(%s);"%(comment.id))).xml()
                admin_delete = (A(T("Delete"), _href='javascript: void(0);', \
                                  _onclick="CommentDelete(%s);"%(comment.id))).xml()            
            else:
                admin_edit=''
                admin_delete=''
            
            author_avatar = DIV(self._get_avatar(comment.author_id))        
            link_reply = A(T("Reply"), _href='javascript: void(0);', \
                           _onclick="ShowReplyBox(%s,%s);" %(id,comment.id))
            comment_inreply = ""           
            #comment_divauthor = '<div class="author"><div class="avatar">%s</div> <div class="name">%s</div> <div class="date">%s</div> <div class="inreply">%s</div>   <div class="id">%s</div><div style="clear: both;"></div> </div>' % (author_avatar.xml(), comment_user, comment_time, comment_inreply, comment.id)
            comment_divauthor = '''<div class="author">
                                    <div class="avatar">%s</div> 
                                    <div class="name">%s</div> 
                                    <div class="date">%s</div> 
                                    <div class="inreply">%s</div>   
                                    <div style="clear: both;"></div> 
                                    </div>''' % (author_avatar.xml(), \
                                                 comment_user, comment_time, \
                                                 comment_inreply)
            comment_divtext = '<div class="response">%s</div>' % MARKMIN(comment.comment)
            comment_divreply = '<div class="menu">%s %s %s</div>' \
                                % (link_reply.xml(), admin_edit, admin_delete)
            list_comments += '<div class="comment" id="comment-%s">%s %s %s</div>' \
                                % (comment.id, comment_divauthor, \
                                   comment_divtext, comment_divreply)
            inc +=1
             
        #get pages
        list_pages = self._get_pages(id,comments_count,page,max_list_per_page)
        if list_pages!="":
            list_comments += list_pages        
                
        info={}
        info['html']=list_comments        
        return sj.dumps(info)



    def _get_avatar(self, userid, style=""):
        
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        db = self.i2p.db
        
        img = IMG(_src=URL(r=request,c='static',f='images/avatar.png'), \
                  alt="User avatar", _title=T('No avatar'), _style=style)
        avatars = db(db.avatars.user_id == userid).select()
        if avatars:
            avatar = avatars[0]
            img_avatar = avatar.image
            if img_avatar:            
                url_avatar = URL(request.application,\
                                 self.i2p.config.controller_default,\
                                 'download',args=[img_avatar])
                img = IMG(_src=url_avatar, alt="User avatar", \
                          _title=avatar.comment[:100],_style=style)
        
        return img   
    
    
    
    def _exist_post(self, id):
        
        db = self.i2p.db
        
        posts = db(db.posts.id == id).select()
        if posts:
            return True
        
        else:
            return False
    
    

    def _exist_reply(self, id):
        
        db = self.i2p.db
        
        comments = db(db.comments.id == id).select()
        if comments:
            return True
        else:
            return False
        
            

    def add(self, id_reply, id_post, value): #_new_comment
        
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        session = self.i2p.environment.session
        db = self.i2p.db
        
        if not self.i2p.config.comments_method in ['Enabled']:
            return json_response(message=T('The comments are disabled'),\
                                 success=0,alert=2)
         
        info={} 
        value_clean = clean_html(value) #clean searching tags
        if value_clean == "":        
            return json_response(message=T('The comment cannot be empty'),\
                                 success=0,alert=2)
        
        user_id = session.auth.user.id
        if user_id <= 0:        
            return json_response(message=T('Problem with user'),\
                                 success=0,alert=2)
        
        if not self._exist_post(id_post):        
            return json_response(message= T("The post you want to comment doesn't exist"),\
                                 success=0,alert=2)
        
        if id_reply != 0:
            if not self._exist_reply(id_reply):        
                return json_response(message= T("The reply you want to comment doesn't exist"),\
                                     success=0,alert=2)
                        
        newidreply = db.comments.insert( post_id = id_post,
                                         author_id = user_id,
                                         reply_id = id_reply,
                                         comment = value_clean                             
                                         )       
        if newidreply>0:        
            return json_response(message=T('Thank you for your reply!'),\
                                 success=1,alert=0)
        else:        
            return json_response(message= T('There was a problem submitting your comment. Try again later.'), \
                                 success=0,alert=2)




    def _get_pages(self, idpost, count, \
                   currentpage,\
                   max_list_per_page=10,\
                   max_display_pages=10):
        import math
        
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
                
            backward = A(T("Prior"), _href='javascript: void(0);', \
                         _onclick="LoadComments(%s,%s);"%(idpost,(currentpage-1)))           
            forward = A(T("Next"), _href='javascript: void(0);', \
                        _onclick="LoadComments(%s,%s);"%(idpost,(currentpage+1)))
                    
            listpages=""    
            if currentpage>1:
                listpages += "<li>%s</li>" % backward.xml()                             
            
            for page in range(first_page, last_page+1):                           
                page_a = A(str(page), _href='javascript: void(0);', \
                           _onclick="LoadComments(%s,%s);"%(idpost,page))            
                if page<=total_pages:
                    if page==currentpage:
                        class_current = ' class="current"'
                    else:
                        class_current = '' 
                    listpages += "<li%s>%s</li>" % (class_current, page_a.xml())            
                
            if total_pages>currentpage:
                listpages += "<li>%s</li>" % forward.xml()
            
            if listpages!="": 
                
                header_comments = T('%s Comments. Page %s of %s') \
                                % (count,currentpage,total_pages)      
                list='<div class="pages"><h2>%s</h2><ul>%s</ul></div>' \
                            % (header_comments, listpages)
        
        return list



class admComments(object): 
        
    def __init__(self, i2p):
        
        self.i2p = i2p
        

    def list(self, currentpage=1, search_text=""):        
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        if not isinstance(search_text, (unicode, str) ): 
            search_text = ""

        max_comments=ADMIN_COMMENTS_LIST_PER_PAGE
        max_display_pages=ADMIN_MAX_LIST_PAGES
        
        limit_inf = (max_comments * currentpage) - max_comments
        limit_sup = limit_inf + max_comments 
        
        count_comments = db(db.comments.id>0).count()
        last_comments = db(db.comments.id>0).select(db.comments.ALL, \
                                                    orderby=~db.comments.comment_on,\
                                                    limitby=(limit_inf, limit_sup))
            
        refresh_list = A(T("Refresh"), _href='javascript: void(0);', \
                         _onclick="CommentsList(1);", \
                         _title="%s"%T('Reload the list'))
        icon_refresh_url = URL(request.application,'static','images/toolbar_refresh.png')    
        toolbar_refresh_style = '''padding-left: 20px; background-image: url(%s); 
                                background-repeat: no-repeat;''' % icon_refresh_url
            
        toolbar_refresh = '<li style="%s">%s</li>' % (toolbar_refresh_style,refresh_list.xml())
        toolbar = '<ul>%s</ul>' % toolbar_refresh    
        list = '<div class="toolbar" style="height: 30px; width: 300px;">%s</div>' % toolbar        
            
        if last_comments: 
            
            checkbox_all = '<input type="checkbox" id="checkboxall" />'
            
            #create the header column   
            caption_column1 = checkbox_all
            caption_column2 = T('Content')
            caption_column3 = T('Article')
            caption_column4 = T('Author')
            caption_column5 = T('Actions')
            caption_column6 = T('Date')
            
            row_column1 = '<div class="column1">%s</div>' % caption_column1
            row_column2 = '<div class="column2">%s</div>' % caption_column2
            row_column3 = '<div class="column3">%s</div>' % caption_column3
            row_column4 = '<div class="column4">%s</div>' % caption_column4
            row_column5 = '<div class="column5">%s</div>' % caption_column5
            row_column6 = '<div class="column6">%s</div>' % caption_column6
            
            row_clear = '<div style="clear: both;"></div>'            
            
            row_article_xml = '<div class="row-comment-headers"> %s %s %s %s %s %s %s </div>' \
                            % (row_column1,row_column2,row_column3,row_column4, \
                               row_column5,row_column6,row_clear)
            list += row_article_xml 
                    
            #titles are hints
            title_edit_comment = T('Click to edit this comment')
            title_delete = T('Click to delete this comment')
            title_link_article = T('Click to go to the article') 
            icon_remove = IMG(_src=URL(request.application,'static','images/remove.png'), \
                              _alt="remove")        
            
            for comment in last_comments: 
                checkbox_comment = '<input type="checkbox" id="checkbox-%s" />'%comment.id
                link_id = A(comment.id, _href='javascript: void(0);', \
                            _onclick="ArticleGoTo(%s);"%(comment.id))
                comment_extract = comment.comment[:50]
                link_comment = A(comment_extract, _href='javascript: void(0);', \
                                 _onclick="CommentEdit(%s);"%(comment.id), \
                                 _title="%s"%title_edit_comment)            
                link_article = self.i2p.articles.get_post_permanent_link(comment.post_id,trunk=True)
                title_author = self.i2p.users.get_user_title(comment.author_id)
                link_author = A(title_author, _href='javascript: void(0);', \
                                _onclick="UserEdit(%s);"%(comment.author_id))            
                link_delete = A(icon_remove, _href='javascript: void(0);', \
                                _onclick="CommentDelete(%s);"%(comment.id), \
                                _title="%s"%title_delete)
                on_date = comment.comment_on.strftime("%Y-%m-%d:%I:%M:%p")            
                
                row_column1 = '<div class="column1">%s</div>' % checkbox_comment
                row_column2 = '<div class="column2">%s</div>' % link_comment.xml()
                row_column3 = '<div class="column3">%s</div>' % link_article.xml()
                row_column4 = '<div class="column4">%s</div>' % link_author.xml()
                row_column5 = '<div class="column5">%s</div>' % link_delete.xml()
                row_column6 = '<div class="column6">%s</div>' % on_date
                row_clear = '<div style="clear: both;"></div>'
                row_comment_xml = '<div class="row-comment" id="row-%s"> %s %s %s %s %s %s %s </div>' \
                            % (comment.id,row_column1,row_column2,row_column3,\
                               row_column4,row_column5,row_column6,row_clear)
               
                #list += sanitate_string(row_comment_xml)
                list += row_comment_xml  
            
            if count_comments>max_comments:
                total_pages = count_comments // max_comments
                if (count_comments % max_comments)>0:
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
                             _onclick="CommentList(%s);"%(currentpage-1))           
                forward = A(T("Next"), _href='javascript: void(0);', \
                            _onclick="CommentList(%s);"%(currentpage+1))
                
                listpages=""    
                if currentpage>1:
                    listpages += "<li>%s</li>" % backward.xml()                             
                
                for page in range(first_page, last_page+1):                
                    page_a = A(unicode(page), _href='javascript: void(0);', \
                               _onclick="CommentList(%s);"%(page))
                    
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
            page_content=list + "%s"%T("No comments")  
              
        html_content = '<h2>%s</h2>'%T("Comments")
        html_content += '%s'%page_content
        info={}          
        info['html']=sanitate_string(html_content)
        return sj.dumps(info)
    


    def delete(self, id):
        
        db = self.i2p.db
        T = self.i2p.environment.T
            
        comments = db(db.comments.id == id).select()
        if comments:
            comment = comments[0]
            id_comment = comment.id  
            db(db.comments.id == id_comment).delete()         
            return json_response(message= T("Comment deleted!") ,\
                                 alert=0,value="")   
        else:
            return json_response(message=T("The comment doesn't exist!"),\
                                 alert=2,value="")
        
        
    def get(self, id):
        
        db = self.i2p.db
        T = self.i2p.environment.T
            
        comments = db(db.comments.id == id).select()
        if comments:
            comment = comments[0]  
            value = comment.comment        
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message=T("The comment doesn't exist!"),\
                                 alert=2,value="")
        
        
    def change(self, id, value):
        
        db = self.i2p.db
        T = self.i2p.environment.T
            
        comments = db(db.comments.id == id).select()
        if comments:
            comment = comments[0]        
            comment.update_record(comment = value)         
            return json_response(message=T("Comment changed") ,\
                                 alert=0,value="")      
        else:
            return json_response(message=T("The comment doesn't exist!"),\
                                 alert=2,value="")




