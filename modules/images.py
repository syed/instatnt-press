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
import cStringIO
import os
import datetime

from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *
from gluon.sql import *
import gluon.contrib.simplejson as sj

#local
from utils import *


ADMIN_IMAGE_LIST_PER_PAGE = 6
ADMIN_MAX_LIST_PAGES = 10
DISABLE_THUMBNAIL = False

class Images(object): 

    
    def __init__(self, i2p):
        
        self.i2p = i2p        
            
        
        
    def define_tables(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        
        db.define_table('images', 
            Field('id', 'id'),   
            Field('blob_key',readable=False,writable=False), #need for gae, because we use blobstore 
                                                             #for the uploaded images             
            Field('comment', 'text', default="",writable=False,readable=False),                
            Field('image','upload', default="", autodelete=True, label=T('Image'),\
                  comment=T('Choose an image ".jpg",".png",".gif" Maximum size: %s px' % \
                            self.i2p.config.upload_max_size)),                                                                                                                              
            Field('thumb','upload', default="", autodelete=True, writable=False,readable=False),
            Field('upload_on', 'datetime', default=datetime.datetime.today(),\
                  writable=False,readable=False),
            migrate=self.i2p.config.is_first_time)
        
        
        
        if request.env.web2py_runtime_gae and self.i2p.config.auto_resize_image: #no IS_IMAGE check in gae, so use RESIZE_IMAGE only
            db.images.image.requires=(RESIZE_IMAGE(environment = self.i2p.environment, \
                                                   nx=self.i2p.config.image_max_size, \
                                                   ny=self.i2p.config.image_max_size, \
                                                   error_message=T('The file you submit is not an image')))            
        elif not self.i2p.config.auto_resize_image:
            db.images.image.requires=(IS_IMAGE(extensions=('jpg','jpeg','png','gif'), \
                                               maxsize=(self.i2p.config.upload_max_size, \
                                                        self.i2p.config.upload_max_size)))
        else:
            db.images.image.requires=(IS_IMAGE(extensions=('jpg','jpeg','png','gif'), \
                                               maxsize=(self.i2p.config.upload_max_size, \
                                                        self.i2p.config.upload_max_size)), \
                                      RESIZE_IMAGE(environment = self.i2p.environment, \
                                                   nx=self.i2p.config.image_max_size, \
                                                   ny=self.i2p.config.image_max_size, \
                                                   error_message=T('The file you submit is not an image')))
            
            
class admImages(object): 

    
    def __init__(self, i2p):
        
        self.i2p = i2p   
            
    
    def list(self, currentpage=1, search_text=""):        
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        if not isinstance(search_text, (unicode, str) ): 
            search_text = ""

        max_images=ADMIN_IMAGE_LIST_PER_PAGE
        max_display_pages=ADMIN_MAX_LIST_PAGES
        
        limit_inf = (max_images * currentpage) - max_images
        limit_sup = limit_inf + max_images 
        
        count_images = db(db.images.id>0).count()
        last_images = db(db.images.id>0).select(db.images.ALL,\
                                                orderby=~db.images.upload_on,\
                                                limitby=(limit_inf, limit_sup))
        
        upload_image = A(T("Upload"), _href='javascript: void(0);', \
                         _onclick="UploadImage();", \
                         _title="%s"%T('Upload an image'))  
        icon_upload_url = URL(request.application,'static','images/toolbar_upload.png')    
        toolbar_upload_style = 'padding-left: 20px; background-image: url(%s); background-repeat: no-repeat;' \
                                % icon_upload_url
        
        refresh_list = A(T("Refresh"), _href='javascript: void(0);', \
                         _onclick="ImageList(1);", \
                         _title="%s"%T('Reload the list'))
        icon_refresh_url = URL(request.application,'static','images/toolbar_refresh.png')    
        toolbar_refresh_style = 'padding-left: 20px; background-image: url(%s); background-repeat: no-repeat;' \
                                % icon_refresh_url
            
        toolbar_upload = '<li style="%s">%s</li>' % (toolbar_upload_style,upload_image.xml())
        toolbar_refresh = '<li style="%s">%s</li>' % (toolbar_refresh_style,refresh_list.xml())
        toolbar = '<ul>%s %s</ul>' % (toolbar_upload,toolbar_refresh)    
        list = '<div class="toolbar" style="height: 30px; width: 300px;">%s</div>' % toolbar        
        
        if last_images:  
            
            icon_link = IMG(_src=URL(request.application,'static','images/linkuploads.png'), \
                            _alt="link", _style="float:left;")
            icon_remove = IMG(_src=URL(request.application,'static','images/remove.png'), \
                              _alt="remove", _style="float:left;")
            icon_comment = IMG(_src=URL(request.application,'static','images/commented.png'), \
                               _alt="Comment")
            
            for image in last_images:                       
                link_id = A(image.id, _href='javascript: void(0);', \
                            _onclick="ShowImage(%s);"%(image.id))
                image_noimg = IMG(_src=self._get_url_image(image.id,True), \
                                  _alt="Thumbnail", \
                                  _style="height: %(size)spx; width: %(size)spx;"%{'size': self.i2p.config.thumbnail_size})
                static_url = self._get_url_image(image.id)            
                link_url = A(icon_link, _href='javascript: void(0);', \
                             _id="link-url-%s"%image.id, \
                             _onclick="ImageShowUrl(%s,'%s');"%(image.id, static_url))                        
                link_delete = A(icon_remove, _href='javascript: void(0);', \
                                _onclick="ImageDelete(%s);"%(image.id))                        
                upload_on = image.upload_on.strftime("%Y-%m-%d at %I:%M %p")
                if image.comment!="":
                    image_title = image.comment[:30]
                else:
                    image_title = T("No title")
                    
                link_title = A(image_title, _href='javascript: void(0);', \
                               _onclick="ImageChangeComment(%s);"%(image.id))
                                        
                row_clear = '<div style="clear: both;"></div>'
                row_column1 = '<div class="icons">%s %s %s</div>' \
                                % (link_url.xml(), link_delete.xml(), row_clear)           
                row_column2 = '<div class="thumb">%s</div>' % image_noimg.xml()
                row_column3 = '<div class="title">%s</div>' % link_title.xml()                       
                row_image_xml = '<div class="thumb-images" id="row-%s"> %s %s %s </div>' \
                                % (image.id, row_column1, row_column2, row_column3)
                list += row_image_xml
            
            list += row_clear
        
            if count_images>max_images:
                total_pages = count_images // max_images
                if (count_images % max_images)>0:
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
                             _onclick="ImageList(%s);"%(currentpage-1))           
                forward = A(T("Next"), _href='javascript: void(0);', \
                            _onclick="ImageList(%s);"%(currentpage+1))
                
                
                listpages=""    
                if currentpage>1:
                    listpages += "<li>%s</li>" % backward.xml()                             
                
                for page in range(first_page, last_page+1):                
                    page_a = A(unicode(page), _href='javascript: void(0);', \
                               _onclick="ImageList(%s);"%(page))
                    
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
            page_content= list + "%s"%T("No images") 
                
        #html_content = '<h2>%s</h2> <div style="height: 350px; width: 800px; overflow-y: scroll;">%s</div>' % (T("Uploaded images"), _utils_sanitate_string(page_content))
        html_content = '<h2>%s</h2>'%T("Uploaded images")
        html_content += "%s"%page_content
        info={}          
        info['html']=sanitate_string(html_content)        
        return sj.dumps(info)  
    
    
    
    #admin view
    def form_upload(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        response = self.i2p.environment.response
        request = self.i2p.environment.request
        session = self.i2p.environment.session
                    
        form = SQLFORM(db.images)
        if form.accepts(request.vars, session):
            self._make_thumbnail(form.vars.id, self.i2p.config.thumbnail_size, 'images')
            response.flash = T('Image uploaded, upload another?')        
            
        return dict(form=form)
        
    
    #admin view
    def delete(self, id): 
        
        db = self.i2p.db
        T = self.i2p.environment.T
               
        images = db(db.images.id == id).select()
        if images:
            image = images[0]
            idimage = image.id
            db(db.images.id == idimage).delete()        
            return json_response(message= T('Image deleted!'),\
                                 alert=0,value="")
        else:        
            return json_response(message=T("This image doesn't exist!"),\
                                 alert=2,value="")
        
        
    #admin view    
    def get_comment(self, id): 
        
        db = self.i2p.db
        T = self.i2p.environment.T
             
        images = db(db.images.id == id).select()
        if images:
            image = images[0]
            value = image.comment        
            return json_response(message="",alert=0,value=value)
        else:
            return json_response(message=T("This image doesn't exist!"),\
                                 alert=2,value="")  

 
    #admin view
    def change_comment(self, id, value):  
        
        db = self.i2p.db
        T = self.i2p.environment.T
          
        images = db(db.images.id == id).select()
        if images:
            image = images[0]        
            image.update_record(comment = value)         
            return json_response(message=T("Image comment changed"),\
                                 alert=0,value="")      
        else:
            return json_response(message=T("This image doesn't exist!"),\
                                 alert=2,value="") 
        
        
    #admin view    
    #from http://www.web2pyslices.com/main/slices/take_slice/62
    #generate thumbnail in local
    def _make_thumbnail_pil(self, image_id, thumb_size, table_name):
        
        try:            
            from PIL import Image
        except: 
            raise ImportError, "Requires PIL installed in your system."
        
        
        db = self.i2p.db
        request = self.i2p.environment.request        
            
        size = (thumb_size, thumb_size)
        upload_images=db(db[table_name].id==image_id).select()
        if upload_images:
            upload_image = upload_images[0]
            url_image = request.folder + 'uploads/' + upload_image.image       
            im=Image.open(url_image)
            im.thumbnail(size,Image.ANTIALIAS)            
            name_without_ext,ext = os.path.splitext(upload_image.image )
            thumb_name='%s_thumb%s' %(name_without_ext, ext)             
            url_thumb = request.folder + 'uploads/' + thumb_name            
            im.save(url_thumb,'jpeg')
            upload_image.update_record(thumb=thumb_name)
            
           
            
    #admin view 
    #generate thumbnail in appengine
    def _make_thumbnail_gae(self, image_id, thumb_size, table_name):
        try:
            from google.appengine.api import images        
        except: 
            raise ImportError, "Problem importing google.appengine.api..."  
        
        db = self.i2p.db
        request = self.i2p.environment.request    
        
        size = (thumb_size, thumb_size)
        upload_images=db(db[table_name].id==image_id).select()
        if upload_images:
            upload_image = upload_images[0]        
            filename, stream = db[table_name].image.retrieve(upload_image.image) 
            data = stream.read()        
            img_resize = images.resize(data, thumb_size, thumb_size, images.JPEG) 
            #save thumbnail jpeg change to .PNG         
            io_thumb = cStringIO.StringIO(img_resize)                           
            upload_image.update_record(thumb=db[table_name].thumb.store(img_resize,filename),\
                                       thumb_blob=io_thumb.read())
            
            
    #admin view                        
    def _make_thumbnail(self, image_id, thumb_size=64, table_name='images'):
        
        db = self.i2p.db
        request = self.i2p.environment.request 
        
        if DISABLE_THUMBNAIL:        
            return    
        if request.env.web2py_runtime_gae:
            self._make_thumbnail_gae(image_id,thumb_size,table_name)
        else:
            self._make_thumbnail_pil(image_id,thumb_size,table_name)
                
                                
    #admin view             
    def _get_url_image(self, image_id, thumb=False):
        
        db = self.i2p.db
        request = self.i2p.environment.request 
        
        if self.i2p.config.fast_download:
            download_controller = 'fast_download'
        else:
            download_controller = 'download'
        
        url_image = ""
        upload_images=db(db.images.id==image_id).select()
        if upload_images:
            upload_image = upload_images[0]
            if not thumb:        
                image_file = upload_image.image
            else:
                image_file = upload_image.thumb
                
            if image_file!="":
                url_image = URL(request.application,\
                                self.i2p.config.controller_default,\
                                download_controller,args=[image_file])
            else:
                url_image = URL(request.application,'static','images/noimage.png')
        else:
            url_image = URL(request.application,'static','images/noimage.png')
            
        return url_image

#saving in appengine blobstore
#this need work, perhaps in a future
#def _response_image(table_name='images',image_size=64):
#    if request.env.web2py_runtime_gae:
#        from google.appengine.ext import blobstore
#        from google.appengine.api import images        
#                
#        if not request.args:
#            raise HTTP(404)        
#        myimages=db(db[table_name].image==request.args[0]).select()
#        if myimages:
#            myimage = myimages[0]            
#            if myimage.blob_key: 
#                if GAE_SERVING_IMAGE:
#                    image_serving = images.get_serving_url(myimage.blob_key,image_size)
#                    return image_serving
#                else:           
#                    blob_info = blobstore.get(myimage.blob_key)            
#                    response.headers['X-AppEngine-BlobKey'] = myimage.blob_key;
#                    response.headers['Content-Type'] = blob_info.content_type;
#                    response.headers['Content-Disposition'] = "attachment; filename=%s" % blob_info.filename
#                    return response.body.getvalue()
#    else:
#        return response.download(request,db)
  



#In appengine using blobstore
#this need work, perhaps in a future
#def _admin_image_form_upload_blobstore(): 
#     
#    if request.env.web2py_runtime_gae: 
#        #this method in Appengine only, because in appengine we use blobstore to save images
#        #I take the slice-code from here: http://www.web2pyslices.com/main/slices/take_slice/63
#        #and I made some changes            
#        from google.appengine.ext import blobstore
#        import uuid
#                  
#        form = SQLFORM(db.images, fields=['image'], upload=URL('image'), showid=False) #generate the form
#        blob_info = None
#        if request.vars.image != None:
#            blob_info = blobstore.parse_blob_info(request.vars.image)
#        
#        myurl = str(URL(request.application,CONTROLLER_ADMIN,'image/form_upload',args=request.args))
#        upload_url = blobstore.create_upload_url(myurl) #from appengine get the upload url        
#        form['_action']=upload_url
#        if form.accepts(request.vars,session,formname="image_form_upload"):
#            #@TODO: can this blob-key update be a post-validation function? 
#            row = db(db.images.id == form.vars.id).select().first()                               
#            if request.vars.image__delete == 'on' or \
#                (form.vars.image != None and (row and row.blob_key)):                    
#                key = row.blob_key
#                blobstore.delete(key) #delete the record in blobstore                  
#                row.update_record(blob_key=None, image=None)
#            if form.vars.image != None:                    
#                filename =  "images.image.%s.jpg" % (str(uuid.uuid4()).replace('-',''))
#                row.update_record(image = filename, blob_key = blob_info.key())            
#                response.flash = T('Image uploaded, upload another?')
#                
#            raise HTTP(303, Location= URL(request.application,CONTROLLER_ADMIN,'image/form_upload'))
#        
#        return form


############################
### AVATARS

class Avatars(object): 

    
    def __init__(self, i2p):
        
        self.i2p = i2p    
               
        
        
    def define_tables(self):
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        db.define_table('avatars', 
            Field('id', 'id'),
            Field('user_id', 'integer',required=True,writable=False,readable=False),
            Field('blob_key',readable=False,writable=False), #need for gae, because we use blobstore 
                                                             #for the uploaded images
            Field('image','upload',default="", autodelete=True, label=T('Image'), \
                  comment=T('Choose an image ".jpg",".png",".gif" Maximum size: %s px'\
                            %self.i2p.config.upload_max_size)),
            Field('url', 'string', length=512, default="",writable=False,readable=False,\
                  label=T('Upload from url')),
            Field('comment', 'text', default="",label=T('Description'),comment=T('* Optional')),
            Field('thumb','upload',  default="", autodelete=True, writable=False,readable=False),                
            Field('upload_on', 'datetime', default=datetime.datetime.today(),writable=False,readable=False),
            Field('up_count', 'integer', default=0,writable=False,readable=False), #counting how many uploads                
            migrate=self.i2p.config.is_first_time)
        
        db.avatars.user_id.requires = IS_IN_DB(db, 'auth_user.id', 'auth_user.email')
        
        if request.env.web2py_runtime_gae: #no IS_IMAGE check in gae, so use RESIZE_IMAGE only            
            db.avatars.image.requires=(RESIZE_IMAGE(environment = self.i2p.environment, \
                                                    nx=self.i2p.config.avatar_size, \
                                                    ny=self.i2p.config.avatar_size, \
                                                    error_message=T('The file you submit is not an image')))
        else:            
            db.avatars.image.requires=(IS_IMAGE(extensions=('jpg','jpeg','png','gif'), \
                                                maxsize=(self.i2p.config.upload_max_size, \
                                                         self.i2p.config.upload_max_size)), \
                                        RESIZE_IMAGE(environment = self.i2p.environment, \
                                                     nx=self.i2p.config.avatar_size, \
                                                     ny=self.i2p.config.avatar_size, \
                                                     error_message=T('The file you submit is not an image')))



