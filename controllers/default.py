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

def index():
    #TODO Check page
        
    try:
        page = int(request.args[0])        
    except:
        page = 1
        
    if page>1:    
        response.front = False   
    else:
        response.front = True
        
    
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules    
           
       
    return dict(page=page)


def page_by_id():
    
    try:        
        post_id = request.args[0]
    except:
        e_message = T("Problem with some submitted values") 
        e_title = T("Error 400!") 
        http_page = pretty_exceptions(e_title,e_message)
        raise HTTP(400, http_page)
    
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules        
        
    response.view='default/view.html'       
    post = i2p.articles.get_article_view_by_id(post_id)                
    if not post:
        e_message = T("Sorry, but this article doesn't exist!") 
        e_title = T("Error 404!") 
        http_page = pretty_exceptions(e_title,e_message)
        raise HTTP(404, http_page)
       
    return dict(post = post)


def page():
    
    try:        
        name = request.args[0]
    except:
        e_message = T("Problem with some submitted values") 
        e_title = T("Error 400!") 
        http_page = pretty_exceptions(e_title,e_message)
        raise HTTP(400, http_page)
    
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules    
        
    response.view='default/view.html'
    post_id = i2p.articles.get_article_id_from_name(name)   
    post = i2p.articles.get_article_view_by_id(post_id)                
    if not post:
        e_message = T("Sorry, but this article doesn't exist!") 
        e_title = T("Error 404!") 
        http_page = pretty_exceptions(e_title,e_message)
        raise HTTP(404, http_page)
         
    return dict(post = post) 


def post():
    
    try: 
        year = request.args[0]
        month = request.args[1]
        day = request.args[2]
        name = request.args[3]
    except:
        e_message = T("Problem with some submitted values") 
        e_title = T("Error 400!") 
        http_page = pretty_exceptions(e_title,e_message)
        raise HTTP(400, http_page)
    
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules    
    
    response.view='default/view.html'
    post_id = i2p.articles.get_article_id_from_date_name(year,month,day,name)   
    post = i2p.articles.get_article_view_by_id(post_id)                
    if not post:
        e_message = T("Sorry, but this article doesn't exist!") 
        e_title = T("Error 404!") 
        http_page = pretty_exceptions(e_title,e_message)
        raise HTTP(404, http_page)
    
        
    return dict(post = post) 
  

def view():    
    
    try: 
        post_id = int(request.args[0])        
    except:
        e_message = T("Problem with id value") 
        e_title = T("Error 400!") 
        http_page = pretty_exceptions(e_title,e_message)
        raise HTTP(400, http_page)
    
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules    
          
    post = i2p.articles.get_article_view_by_id(post_id)                
    if not post:   
        e_message = T("Sorry, but this article doesn't exist!") 
        e_title = T("Error 404!") 
        http_page = pretty_exceptions(e_title,e_message)
        raise HTTP(404, http_page)
    
    return dict(post = post) 


def preview():   
    
    if not check_credentials_is_admin(): #admin only
        return
     
    try: 
        post_id = int(request.args[0])        
    except:
        e_message = T("Problem with id value") 
        e_title = T("Error 400!") 
        http_page = pretty_exceptions(e_title,e_message)
        raise HTTP(400, http_page)
    
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules    
    
    response.view='default/view.html'      
    post = i2p.articles.get_article_view_by_id(post_id,preview=True)                
    if not post:   
        e_message = T("Sorry, but this article doesn't exist!") 
        e_title = T("Error 404!") 
        http_page = pretty_exceptions(e_title,e_message)
        raise HTTP(404, http_page)
        
    return dict(post = post)


def category(): 
    
    try:
        subarea = request.args[0]        
    except:        
        e_message = T("This function doesn't exist!") 
        e_title = T("Error 400!") 
        http_page = pretty_exceptions(e_title,e_message)
        raise HTTP(400, http_page)
    
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules    
    
    if subarea=="by_id":        
        try:
            category = int(request.args[1])               
        except:
            e_message = T("Problem with categorie id value!") 
            e_title = T("Error 400!") 
            http_page = pretty_exceptions(e_title,e_message)
            raise HTTP(400, http_page)            
                        
        try:
            page = int(request.vars.page)        
        except:
            page = 1
        
        (posts, count_posts) = i2p.articles.get_last_posts_with_cat_id(page,category)       
        xml_posts = i2p.articles.get_xml_results_from_posts(posts)
        xml_pages = i2p.articles.pagination_last_post_cat(page, count_posts, category)   
                
        return dict(page=page, category=category, posts=posts, count_posts=count_posts, \
                    xml_posts=xml_posts, xml_pages=xml_pages)     
      
    else:
        e_message = T("This function doesn't exist!") 
        e_title = T("Error 400!") 
        http_page = pretty_exceptions(e_title,e_message)
        raise HTTP(400, http_page)


def tag(): 
       
    try:
        tag = request.args[0]        
    except:        
        e_message = T("This function doesn't exist!") 
        e_title = T("Error 400!") 
        http_page = pretty_exceptions(e_title,e_message)
        raise HTTP(400, http_page)
    
    try:
        page = int(request.vars.page)        
    except:
        page = 1
        
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules    
        
    (posts, count_posts) = i2p.articles.get_last_posts_with_tag_name(page,tag)       
    xml_posts = i2p.articles.get_xml_results_from_posts(posts)
    xml_pages = i2p.articles.pagination_last_post_tag(page, count_posts, tag)        

    return dict(page=page, tag=tag, posts=posts, count_posts=count_posts, \
                xml_posts=xml_posts, xml_pages=xml_pages) 



def archives():  
    
    import datetime
      
    try:
        year = int(request.args[0])
        month = int(request.args[1])  
        d_lower=datetime.date(year,month,1)      
    except:
        e_message = T("There was a problem with values of Year - Month") 
        e_title = T("Error 400!") 
        http_page = pretty_exceptions(e_title,e_message)
        raise HTTP(400, http_page)
    
    try:
        page = int(request.vars.page)        
    except:
        page = 1 
        
    
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules    
        
    (posts, count_posts) = i2p.articles.get_last_posts_archives_monthyear(page,year,month)       
    xml_posts = i2p.articles.get_xml_results_from_posts(posts)
    xml_pages = i2p.articles.pagination_archive_monthyear(page, count_posts, year, month) 
     
    return dict(year=year, month=month, page=page, posts=posts, count_posts=count_posts, \
                xml_posts=xml_posts, xml_pages=xml_pages)        


def search(): 
       
    try:
        qvalue = request.vars.q        
    except:
        e_title = T("Error 400!")
        e_message = T("You need to submit your search text.")         
        http_page = pretty_exceptions(e_title,e_message)
        raise HTTP(400, http_page)
    
    try:
        page = int(request.vars.page)        
    except:
        page = 1
        
    
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules    
    
    (posts, count_posts) = i2p.articles.get_last_posts_with_search(page,qvalue)       
    xml_posts = i2p.articles.get_xml_results_from_posts(posts)
    xml_pages = i2p.articles.pagination_last_post_search(page, count_posts, qvalue)        
        
    return dict(page=page, qvalue=qvalue, posts=posts, count_posts=count_posts, \
                xml_posts=xml_posts, xml_pages=xml_pages)
        

################
## FEEDS ######
###############

@cache(request.env.path_info, time_expire=CACHE_TIME_EXPIRE_PAGES, cache_model=cache.ram)
def feed_articles():
        
    #begin load custom modules
    i2p.load_mod_siteinfo()
    i2p.load_mod_articles()    
    i2p.define_siteinfo()
    i2p.define_articles()    
    #end load custom modules
        
    return response.render(i2p.articles.generate_rss_last_posts())

@cache(request.env.path_info, time_expire=CACHE_TIME_EXPIRE_PAGES, cache_model=cache.ram)
def feed_comments():
    
    #begin load custom modules
    i2p.load_mod_users()
    i2p.load_mod_siteinfo()
    i2p.load_mod_articles() 
    i2p.load_mod_comments()   
    i2p.define_siteinfo()
    i2p.define_articles() 
    i2p.define_comments()   
    #end load custom modules
        
    return response.render(i2p.articles.generate_rss_last_comments())


###########################
#json controllers
############################

@cache(request.env.path_info, time_expire=CACHE_TIME_EXPIRE_JSON, cache_model=cache.ram)
def json_get_sidebar_categories():
    session.forget()
        
    #begin load custom modules
    i2p.load_mod_categories()
    i2p.load_mod_articles()
    i2p.load_mod_widgets() 
    i2p.define_categories()
    i2p.define_articles()    
    #end load custom modules  
    
    info={}          
    info['html']=i2p.widgets.load_categories()        
    import gluon.contrib.simplejson as sj
    return sj.dumps(info)

@cache(request.env.path_info, time_expire=CACHE_TIME_EXPIRE_JSON, cache_model=cache.ram)
def json_get_sidebar_last_posts():
    session.forget()
    
    #begin load custom modules
    i2p.load_mod_articles()
    i2p.load_mod_widgets() 
    i2p.define_articles()
    #end load custom modules
    
    info={}          
    info['html']=i2p.widgets.load_last_posts()    
    import gluon.contrib.simplejson as sj
    return sj.dumps(info)    

@cache(request.env.path_info, time_expire=CACHE_TIME_EXPIRE_JSON, cache_model=cache.ram)
def json_get_sidebar_tags():
    session.forget()
            
    #begin load custom modules
    i2p.load_mod_articles()     
    i2p.define_articles()
    #end load custom modules    
    
    info={}          
    info['html']=i2p.articles.get_popular_tags()       
    import gluon.contrib.simplejson as sj
    return sj.dumps(info)

@cache(request.env.path_info, time_expire=CACHE_TIME_EXPIRE_JSON, cache_model=cache.ram)
def json_get_sidebar_pages():
    session.forget()
      
    #begin load custom modules
    i2p.load_mod_articles()
    i2p.load_mod_widgets() 
    i2p.define_articles()
    #end load custom modules
    
    info={}          
    info['html']=i2p.widgets.get_pages()        
    import gluon.contrib.simplejson as sj
    return sj.dumps(info)

@cache(request.env.path_info, time_expire=CACHE_TIME_EXPIRE_JSON, cache_model=cache.ram)
def json_get_sidebar_archive():
    session.forget()
        
    #begin load custom modules
    i2p.load_mod_articles()  
    i2p.define_articles()
    #end load custom modules  
    
    info={}          
    info['html']=i2p.articles.get_list_archives()         
    import gluon.contrib.simplejson as sj
    return sj.dumps(info)

@cache(request.env.path_info, time_expire=CACHE_TIME_EXPIRE_JSON, cache_model=cache.ram)
def json_get_sidebar_links():
    session.forget()
    
    #begin load custom modules     
    i2p.load_mod_articles()   
    i2p.load_mod_links()
    i2p.define_links()
    #end load custom modules
    
    info={}          
    info['html']=i2p.articles.get_list_links()           
    import gluon.contrib.simplejson as sj
    return sj.dumps(info)

@cache(request.env.path_info, time_expire=CACHE_TIME_EXPIRE_JSON, cache_model=cache.ram)
def json_get_sidebar_last_comments():
    session.forget()
            
    #begin load custom modules
    i2p.load_mod_users()
    i2p.load_mod_articles()
    i2p.load_mod_comments()
    i2p.load_mod_widgets() 
    i2p.load_mod_images()
    i2p.define_articles()
    i2p.define_comments()
    i2p.define_avatars()
    #end load custom modules        
    
    info={}          
    info['html']=i2p.widgets.load_last_comments()        
    import gluon.contrib.simplejson as sj
    return sj.dumps(info)

def json_get_comments_count():
    session.forget()
       
    #begin load custom modules    
    i2p.load_mod_comments()     
    i2p.define_comments()   
    #end load custom modules
    
    try:
        id = int(request.vars.id)                
    except:
        return json_response(message= T("The comment id doesn't exist"),\
                             success=0,alert=2)
    else:        
        return i2p.comments.count(id)   


def json_get_comments_title():
    session.forget()
            
    #begin load custom modules
    i2p.load_mod_articles()
    i2p.load_mod_comments() 
    i2p.define_articles()
    i2p.define_comments()   
    #end load custom modules    
    
    try:
        id = int(request.vars.id)                
    except:
        return json_response(message= T("The article id or page number doesn't exist"),\
                             success=0,alert=2)
    else:        
        return i2p.comments.generate_title(id)   

def json_get_comments_form():
        
    #begin load custom modules
    i2p.load_mod_users()
    i2p.load_mod_comments()   
    #end load custom modules
    
    try:
        id = int(request.vars.id)                
    except:
        return json_response(message= T("The article id doesn't exist"),\
                             success=0,alert=2)
    else:        
        return i2p.comments.generate_reply(id)   


def json_get_comments_from_post():
    session.forget()
    
    #begin load custom modules
    i2p.load_mod_users()
    i2p.load_mod_articles()
    i2p.load_mod_comments()
    i2p.load_mod_widgets() 
    i2p.load_mod_images()
    i2p.define_articles()
    i2p.define_comments()
    i2p.define_avatars()
    #end load custom modules
    
    try:
        id = int(request.vars.id)
        page = int(request.vars.page)        
    except:
        return json_response(message= T("The article id or page number doesn't exist"),\
                             success=0,alert=2)
    else:        
        return i2p.comments.get_all(id,page)   

def json_get_comments_from_post_admin(): 
    
    #begin load custom modules
    i2p.load_mod_users()
    i2p.load_mod_articles()
    i2p.load_mod_comments()
    i2p.load_mod_widgets() 
    i2p.load_mod_images()
    i2p.define_articles()
    i2p.define_comments()
    i2p.define_avatars()
    #end load custom modules
       
    if not check_credentials_is_admin():
        return _common_json_response(message= T("You need to sign in as an admin"),\
                                     success=0,alert=2)    
    try:
        id = int(request.vars.id)
        page = int(request.vars.page)        
    except:           
        return json_response(message= T("The article id or page number doesn't exist"),\
                             success=0,alert=2)    
    else:        
        return i2p.comments.get_all(id,page,True)   

def json_check_user_is_log_in():
    
    value = False
    if is_user_logged_in():                    
        value = True       
        
    info={}
    info['value']=value          
    import gluon.contrib.simplejson as sj
    return sj.dumps(info)    

@auth.requires_login()
def json_new_comment():
            
    #begin load custom modules
    i2p.load_mod_articles()
    i2p.load_mod_comments()
    i2p.define_articles()
    i2p.define_comments() 
    #end load custom modules   
    
    try:
        id_reply = int(request.vars.idreply)
        id_post = int(request.vars.idpost)
        value = request.vars.value        
    except:
        return json_response(message= T("The article id, page number, or reply doesn't exist"), \
                             success=0,alert=2)
    else:        
        return i2p.comments.add(id_reply,id_post,value)     
  

##################################
###### USER ACTIONS ##############
##################################
#this change the avatar user and generate the current thumbnail of the image

@auth.requires_login()
def change_avatar():
    import datetime
    
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules 
      
    if not i2p.config.avatars_enabled:
        e_title = T("Error 400!")
        e_message = T("Avatars are disable.")         
        http_page = pretty_exceptions(e_title,e_message)
        raise HTTP(400, http_page)         
    
    user_id = session.auth.user.id
    avatars = db(db.avatars.user_id == user_id).select()
    if not avatars:
        newid = db.avatars.insert(user_id=user_id)
        avatars = db(db.avatars.user_id == user_id).select()  
          
    if avatars:
        avatar = avatars[0]        
        form = SQLFORM(db.avatars, avatar, upload=URL('download'), showid=False)
        if form.accepts(request.vars, session):                        
            response.flash = T('Avatar uploaded') 
            redirect(URL('index'))
                               
        return dict(form=form)
    
    else:
        e_title = T("Error 400!")
        e_message = T("Problem with avatars")         
        http_page = pretty_exceptions(e_title,e_message)
        raise HTTP(400, http_page) 
 
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    i2p.load_mod_images()
    i2p.define_images()
    i2p.define_avatars()
    
    return response.download(request,db)


def fast_download():
    
    i2p.load_mod_images()
    i2p.define_images()
    i2p.define_avatars()
    
    # very basic security (only allow fast_download on your_table.upload_field):
    if not request.args(0).startswith("images.image"):
        return download()
    elif not request.args(0).startswith("images.thumb"):
        return download()
    
    if not request.args(0).startswith("avatars.image"):
        return download()
    elif not request.args(0).startswith("avatars.thumb"):
        return download()
    
    # remove/add headers that prevent/favors client-side caching
    del response.headers['Cache-Control']
    del response.headers['Pragma']
    del response.headers['Expires']
    filename = os.path.join(request.folder,'uploads',request.args(0))
    # send last modified date/time so client browser can enable client-side caching
    response.headers['Last-Modified'] = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(os.path.getmtime(filename)))
    return response.stream(open(filename,'rb'))
    
def user():
    
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules    
    
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())




