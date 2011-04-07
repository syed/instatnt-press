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
from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *
import gluon.contrib.simplejson as sj
import re


def clean_html(text):
    pattern = re.compile(r'<.*?>') 
    result_text = pattern.sub('', text)        
    return result_text

def _utils_strip_list(l):
    return([x.strip() for x in l])

def sanitate_string(text,method='replace'):    
    if type(text)!=unicode:
        sanitate_string = unicode(text,'utf-8',method)
    else:
        sanitate_string = text
    
    return sanitate_string


def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.
    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if isinstance(s, str):
        return unicode(s).encode(encoding, errors)
    elif not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only,
                        errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s

def json_response(message="",alert=0,value="",success=0):
    info={}          
    info['message']=str(message)
    info['success']=success
    info['alert']=alert
    info['value']=value   
    return sj.dumps(info)

def get_query_limits(page, max_list_per_page): 
      
    limit_inf = (max_list_per_page * page) - max_list_per_page
    limit_sup = limit_inf + max_list_per_page
    
    return (limit_inf, limit_sup)


class RESIZE_IMAGE: 
    
    def __init__(self, environment, nx=800, ny=800, \
                 error_message='The file you submit is not an image'): 
        self.environment = environment
        self.nx = nx
        self.ny = ny
        self.error_message = error_message 
          
    def __call__(self, value): 
        
        request = self.environment.request
        
        if isinstance(value, str) and len(value)==0: 
            return (value,None) 
        
        if request.env.web2py_runtime_gae:
            from google.appengine.api import images 
            import cStringIO 
            try: 
                img_resize = images.resize(value.file.read(), \
                                           self.nx, self.ny, images.JPEG) #jpeg image 
                value.file = cStringIO.StringIO(img_resize) 
                return (value, None) 
            except: 
                return (value, self.error_message)
            
        else:          
            
            from PIL import Image
            import cStringIO      
            
            try:                
                imgData = Image.open(cStringIO.StringIO(value.file.read())).convert("RGB") 
                imgData.thumbnail((self.nx, self.ny), Image.ANTIALIAS) 
                thumbFile = cStringIO.StringIO() 
                imgData.save(thumbFile, "JPEG", quality=85) 
                thumbFile.seek(0) 
                value.file = thumbFile                
            except: 
                return (value, self.error_message)
            else:
                return (value, None)



