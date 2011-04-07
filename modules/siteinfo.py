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
import os

from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *
from gluon.sql import *
import gluon.contrib.simplejson as sj

#local
from utils import *


AVATAR_MAX_SIZE = 160 #pixels show in profile and store
AVATAR_SIZE = 48 #32 pixels is the pixels show in comments
THUMBNAIL_SIZE = 160 # 64 pixels
IMAGE_MAX_SIZE = 800 #800 pixels
UPLOAD_MAX_SIZE = 1600 #maximum pixel size of the upload image, yes 
                       #if you have more pixels than this you have to resize before.


class SiteInfo(object): 
    
    def __init__(self, i2p):
        
        self.i2p = i2p        
                
        
    def define_tables(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request

        db.define_table('siteinfo',                                  
            Field('id', 'id'),
            Field('site_title', 'string', length=255, default=""), 
            Field('site_subtitle', 'string', length=255, default=""),                                      
            Field('site_description', 'text', default=""),
            Field('site_front', 'text', default=""),
            Field('site_aboutme', 'text', default=""),
            Field('site_keywords', 'text', default=""),
            Field('site_footer', 'text', default=""),
            Field('site_logo', 'text', default=""),
            Field('site_css', 'text', default=""),
            Field('site_url', 'text', default="",requires=(IS_URL())),
            Field('site_layout', 'string', length=255, default=""),
            Field('site_language', 'string', length=255, default=""),                                                                                                            
            migrate=self.i2p.config.is_first_time  ) #self.i2p.config.is_first_time         
                
        


    def no_info_in_db(self):
        
        db = self.i2p.db
                
        noinfo=True        
        siteinfo = db(db.siteinfo.id>0).select()
        if siteinfo:
            noinfo = False
        return noinfo


    def _get_title(self):
        
        db = self.i2p.db
                
        siteinfo = db(db.siteinfo.id>0).select()
        if siteinfo:
            title = siteinfo[0].site_title
        else:
            title = ""
        
        return title


    def _get_subtitle(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        siteinfo = db(db.siteinfo.id>0).select()
        if siteinfo:
            subtitle = siteinfo[0].site_subtitle
        else:
            subtitle = T("No subtitle")
        
        return subtitle


    
    def _get_description(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        siteinfo = db(db.siteinfo.id>0).select()
        if siteinfo:
            description = siteinfo[0].site_description
        else:
            description = ""
        
        return description
    


    def _get_frontpage(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        siteinfo = db(db.siteinfo.id>0).select()
        if siteinfo:
            description = siteinfo[0].site_front
        else:
            description = T("No description")
        
        return description
    
    
    
    def _get_aboutme(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        siteinfo = db(db.siteinfo.id>0).select()
        if siteinfo:
            site_aboutme = siteinfo[0].site_aboutme
        else:
            site_aboutme = T("No text")
        
        return site_aboutme
    


    def _get_keywords(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        siteinfo = db(db.siteinfo.id>0).select()
        if siteinfo:
            keywords = siteinfo[0].site_keywords
        else:
            keywords = ""
        
        return keywords



    def _get_css(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        siteinfo = db(db.siteinfo.id>0).select()
        if siteinfo:
            css = siteinfo[0].site_css
        else:
            css = ""
        
        return css
    
    

    def _get_footer(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        siteinfo = db(db.siteinfo.id>0).select()
        if siteinfo:
            description = siteinfo[0].site_footer
        else:
            description = ""
        
        return description



    def _get_logo_url(self):
        
        db = self.i2p.db        
        request = self.i2p.environment.request
        
        siteinfo = db(db.siteinfo.id>0).select()
        if siteinfo:
            logo_url = siteinfo[0].site_logo
            if logo_url == "":
                logo_url = URL(request.application,'static','images/mylogo.png')
        else:
            logo_url = URL(request.application,'static','images/mylogo.png')
        
        return logo_url
    
    

    def print_style_css(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        site_css = self._get_css()
        site_css_xml = '<style type="text/css" charset="utf-8">%s</style>' % site_css
        return XML(site_css_xml)
    
    
    
    def print_logo(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        site_logo_url = self._get_logo_url()
        logo_img = IMG(_src=site_logo_url, _alt="Logo Site")  
        logo_img_link = A(logo_img, _href=URL(request.application,\
                                              self.i2p.config.controller_default,\
                                              'index'),\
                          _style="border:none;", \
                          _title="%s"%T("Go back to main page"))
          
        return XML(logo_img_link.xml())



    def _get_layout(self):
        
        db = self.i2p.db
                
        layout = "default"
        siteinfo = db(db.siteinfo.id>0).select()
        if siteinfo:
            site_layout = siteinfo[0].site_layout
            if site_layout != "":
                layout = site_layout    
                
        return layout
    
    
    def _get_default_style(self, layout = 'default'):
        
        request = self.i2p.environment.request
        
        path_styles =os.path.join(request.folder,'views/styles/') #get the full path to layouts                
        
                    
        css=""
        try: #get the css style from file
            file_style = os.path.join(path_styles, layout, 'style.css')
            file = open(file_style)
            for line in file:
                css += line
            file.close()
        except:
            pass
                        
        return css    
    
    
    def _get_current_view(self):
        
        response = self.i2p.environment.response      
        
        view = 'default' #the default view      
        if response.view=='default/index.html':
            view = 'index'
        elif response.view=='default/view.html':
            view = 'view'
        elif response.view=='default/archive.html' or  \
             response.view=='default/search.html' or  \
             response.view=='default/category.html' or \
             response.view=='default/tag.html':
                view = 'search'
        
        return view   


    def get_layout_header(self):  
                    
        view = self._get_current_view()    
        url_to_layout = 'styles/%s/%s/header.html' % (self._get_layout(), view)         
        return url_to_layout  
    
    
    def get_layout_footer(self): 
        
        view = self._get_current_view()        
        url_to_layout = 'styles/%s/%s/footer.html' % (self._get_layout(), view)    
        return url_to_layout

    
    def get_layout_sidebar(self):
        
        view = self._get_current_view()        
        url_to_layout = 'styles/%s/%s/sidebar.html' % (self._get_layout(), view)    
        return url_to_layout
    
    
    def get_layout_css(self):  
        
        view = self._get_current_view()
        url_to_layout = 'styles/%s/%s/_css.html' % (self._get_layout(), view)         
        return url_to_layout
    


class admSiteInfo(object): 
    
    def __init__(self, i2p):
        
        self.i2p = i2p        
    
    #Admin    
    def list(self):
        
        T = self.i2p.environment.T  
        request = self.i2p.environment.request      
        
        info={} 
    
        caption_customize = T('Change site information') 
        caption_title = T('Title')
        caption_subtitle = T('Subtitle')
        caption_description = T('Description')
        caption_frontpage = T('Front Page')
        caption_about = T('About')
        caption_keywords = T('Keywords')
        caption_copyright = T('Footer')
        caption_logo = T('Logo')
        
        #titles are hints
        title_change_title = T('Click to change the title of the site')
        title_change_subtitle = T('Click to change the subtitle of the site')
        title_change_description = T('Click to change the description of the site')
        title_change_frontpage = T('Click to change the frontpage of the site')
        title_change_about = T('Click to change about content')
        title_change_keywords = T('Click to change keywords of the site')
        title_change_footer = T('Click to change footer content')
        title_change_logo = T('Click to change the logo')
        
        icon_info = IMG(_src=URL(request.application,'static','images/special.png'), \
                        _alt="Info",_style="float:left;")
        link_title = A(caption_title, _href='javascript: void(0);', \
                       _onclick="InfoChangeTitle();", _style="padding-left: 5px;", \
                       _title="%s"%title_change_title)
        link_subtitle = A(caption_subtitle, _href='javascript: void(0);', \
                          _onclick="InfoChangeSubTitle();", _style="padding-left: 5px;", \
                          _title="%s"%title_change_subtitle)
        link_description = A(caption_description, _href='javascript: void(0);', \
                             _onclick="InfoChangeDescription();", \
                             _style="padding-left: 5px;", \
                             _title="%s"%title_change_description)
        link_frontpage = A(caption_frontpage, _href='javascript: void(0);', \
                           _onclick="InfoChangeFrontPage();", _style="padding-left: 5px;", \
                           _title="%s"%title_change_frontpage)
        link_about = A(caption_about, _href='javascript: void(0);', \
                       _onclick="InfoChangeAbout();", _style="padding-left: 5px;", \
                       _title="%s"%title_change_about)
        link_keywords = A(caption_keywords, _href='javascript: void(0);', \
                          _onclick="InfoChangeKeywords();", _style="padding-left: 5px;", \
                          _title="%s"%title_change_keywords)
        link_copyright = A(caption_copyright, _href='javascript: void(0);', \
                           _onclick="InfoChangeFooter();", _style="padding-left: 5px;", \
                           _title="%s"%title_change_footer)
        link_logo = A(caption_logo, _href='javascript: void(0);', \
                      _onclick="InfoChangeLogo();", _style="padding-left: 5px;", \
                      _title="%s"%title_change_logo)
               
        actions = '''<h2>%s</h2>
                    <ul>
                    <li>%s</li>
                    <li>%s</li>
                    <li>%s</li>
                    <li>%s</li>                
                    <li>%s</li>
                    <li>%s</li>
                    <li>%s</li>
                    <li>%s</li>
                    </ul>''' % (caption_customize, link_title.xml(), link_subtitle.xml(), \
                                link_description.xml(), link_frontpage.xml(), \
                                link_about.xml(), link_keywords.xml(), link_copyright.xml(), \
                                link_logo.xml())  
                     
        info['html']=actions        
        return sj.dumps(info)
    
         
    def get_title(self):
            
        
        info={}          
        info['value']=self.i2p.siteinfo._get_title()
        info['message']=""
        info['alert']=0
        
        return sj.dumps(info)
    
    
     
    def get_subtitle(self):
        
                
        info={}          
        info['value']=self.i2p.siteinfo._get_subtitle()
        info['message']=""
        info['alert']=0           
        
        return sj.dumps(info)


     
    def get_description(self):
        
                
        info={}          
        info['value']=self.i2p.siteinfo._get_description()
        info['message']=""
        info['alert']=0           
        
        return sj.dumps(info)
    
     
    def get_frontpage(self):
        
        
        info={}          
        info['value']=self.i2p.siteinfo._get_frontpage()
        info['message']=""
        info['alert']=0           
        
        return sj.dumps(info)
    
         
    def get_about(self):
        
                
        info={}          
        info['value']=self.i2p.siteinfo._get_aboutme()
        info['message']=""
        info['alert']=0           
        
        return sj.dumps(info)

    
     
    def get_keywords(self):
        
    
        
        info={}          
        info['value']=self.i2p.siteinfo._get_keywords()
        info['message']=""
        info['alert']=0           
        
        return sj.dumps(info)


     
    def get_copyright(self):
        
                
        info={}          
        info['value']=self.i2p.siteinfo._get_footer()
        info['message']=""
        info['alert']=0           
        
        return sj.dumps(info)

     
    def get_logo(self):
        
                
        info={}          
        info['value']=str(self.i2p.siteinfo._get_logo_url())
        info['message']=""
        info['alert']=0           
        
        return sj.dumps(info)
    

     
    def save_logo(self, value):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        (url, notvalid) = (IS_URL()(value))
        if notvalid:
            return json_response(message=T("The url to logo is not valid use: http://www.mysite.com/mylogo.png"), \
                                 alert=2,value="")
        
        info={}          
        info['message']=sanitate_string("%s"%T('Logo url updated, now reload the page to see the changes'))
        info['alert']=0 
        siteinfo = db(db.siteinfo.id>0).select()
        if siteinfo:
            myinfo = siteinfo[0]   
            myinfo.update_record(site_logo = url)
        
        return sj.dumps(info)
    

     
    def save_title(self, value):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        info={}          
        info['message']=sanitate_string("%s"%T('Title updated, now reload the page to see the changes'))
        info['alert']=0 
        siteinfo = db(db.siteinfo.id>0).select()
        if siteinfo:
            myinfo = siteinfo[0]   
            myinfo.update_record(site_title = value)
                  
        
        return sj.dumps(info)


     
    def save_subtitle(self, value):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        info={}          
        info['message']=sanitate_string("%s"%T('Subtitle updated, now reload the page to see the changes'))
        info['alert']=0 
        siteinfo = db(db.siteinfo.id>0).select()
        if siteinfo:
            myinfo = siteinfo[0]   
            myinfo.update_record(site_subtitle = value)
                  
        
        return sj.dumps(info)


     
    def save_description(self, value):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        info={}          
        info['message']=sanitate_string("%s"%T('Description updated, now reload the page to see the changes'))
        info['alert']=0 
        siteinfo = db(db.siteinfo.id>0).select()
        if siteinfo:
            myinfo = siteinfo[0]   
            myinfo.update_record(site_description = value)
                  
        
        return sj.dumps(info)


 
    def save_frontpage(self, value):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
                
        info={}          
        info['message']=sanitate_string("%s"%T('Front page updated, now reload the page to see the changes'))
        info['alert']=0 
        siteinfo = db(db.siteinfo.id>0).select()
        if siteinfo:
            myinfo = siteinfo[0]   
            myinfo.update_record(site_front = value)
                  
        
        return sj.dumps(info)


     
    def save_about(self, value):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
                
        info={}          
        info['message']=sanitate_string("%s"%T('About updated, now reload the page to see the changes'))
        info['alert']=0 
        siteinfo = db(db.siteinfo.id>0).select()
        if siteinfo:
            myinfo = siteinfo[0]   
            myinfo.update_record(site_aboutme = value)
                  
        
        return sj.dumps(info)


    
    def save_keywords(self, value):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
        info={}          
        info['message']=sanitate_string("%s"%T('Keywords updated, now reload the page to see the changes'))
        info['alert']=0 
        siteinfo = db(db.siteinfo.id>0).select()
        if siteinfo:
            myinfo = siteinfo[0]   
            myinfo.update_record(site_keywords = value)
                  
        
        return sj.dumps(info)



    def save_copyright(self, value):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        
                
        info={}          
        info['message']=sanitate_string("%s"%T('Footer updated, now reload the page to see the changes'))
        info['alert']=0 
        siteinfo = db(db.siteinfo.id>0).select()
        if siteinfo:
            myinfo = siteinfo[0]   
            myinfo.update_record(site_footer = value)
                  
        
        return sj.dumps(info)


        
        