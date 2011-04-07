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


def articles():
    
    if not check_credentials_is_admin():
        return
    
    try:
        subarea = request.args[0]        
    except:
        return json_response(message=T("Problem with the values submitted"),\
                             alert=2,value="")
 
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules    
    
    i2p.load_mod_articles_admin() #load admin_articles
    i2p.load_mod_categories_admin() #load admin categories we need this too
    i2p.load_mod_tags_admin() #load admin tags we need this too
    
    if subarea=="list": 
        
        
        try:
            search_text = request.vars.search        
        except:
            search_text = "" 
               
        try:
            page = int(request.vars.page)        
        except:
            page = 1 
        
        
        return i2p.admin_articles.list(page,search_text)  
        
    
    elif subarea=="add":        
        
        return i2p.admin_articles.add()                
            
    elif subarea=="delete":
        
        try:
            id = int(request.vars.id)                 
        
        except:            
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")        
        else:                         
            return i2p.admin_articles.delete(id)       
            
    
    elif subarea=="change_title":
        
        try:
            id = int(request.vars.id) 
            value = request.vars.value                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:
            
            return i2p.admin_articles.change_title(id, value)            
            
        
    elif subarea=="get_title":            
        
        try:
            id = int(request.vars.id)                                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:            
            return i2p.admin_articles.get_title(id)            
            
    
    elif subarea=="change_content":
        
        try:
            id = int(request.vars.id) 
            value = request.vars.value                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:            
            return i2p.admin_articles.change_content(id, value)                        
            
        
    elif subarea=="get_content":            
        
        try:
            id = int(request.vars.id)                                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:            
            return i2p.admin_articles.get_content(id)        
            
    
    elif subarea=="change_extract":
        
        try:
            id = int(request.vars.id) 
            value = request.vars.value                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:            
            return i2p.admin_articles.change_extract(id,value)            
            
        
    elif subarea=="get_extract":            
        
        try:
            id = int(request.vars.id)                                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:            
            return i2p.admin_articles.get_extract(id) 
                    
    
    elif subarea=="change_keywords":
        
        try:
            id = int(request.vars.id) 
            value = request.vars.value                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:            
            return i2p.admin_articles.change_keywords(id,value)            
            
        
    elif subarea=="get_keywords":            
        
        try:
            id = int(request.vars.id)                                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:            
            return i2p.admin_articles.get_keywords(id)        
            
        
    elif subarea=="change_url":
        
        try:
            id = int(request.vars.id) 
            value = request.vars.value                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:            
            return i2p.admin_articles.change_url(id,value)            
            
        
    elif subarea=="get_url":            
        
        try:
            id = int(request.vars.id)                                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:            
            return i2p.admin_articles.get_url(id)         
            

    elif subarea=="change_name":
        
        try:
            id = int(request.vars.id) 
            value = request.vars.value                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:            
            return i2p.admin_articles.change_name(id,value)             
            
        
    elif subarea=="get_name":            
        
        try:
            id = int(request.vars.id)                                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:           
            return i2p.admin_articles.get_name(id)        
            

    elif subarea=="change_status":
        
        try:
            id = int(request.vars.id) 
            value = int(request.vars.value)                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:            
            return i2p.admin_articles.change_status(id,value)    
            
        
    elif subarea=="get_status":            
        
        try:
            id = int(request.vars.id)                                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:            
            return i2p.admin_articles.get_status(id) 
            

    elif subarea=="change_ispage":
        
        try:
            id = int(request.vars.id) 
            value = int(request.vars.value)                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:  
            return i2p.admin_articles.change_ispage(id,value)          
            
        
    elif subarea=="get_ispage":            
        
        try:
            id = int(request.vars.id)                                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:  
            return i2p.admin_articles.get_ispage(id)      
                    
    
    elif subarea=="get_categories":            
        
        try:
            id = int(request.vars.id)                                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:        
            return i2p.admin_categories.get_list_from_article(id)
            
        
    elif subarea=="change_categories":
        
        try:            
            id = int(request.vars.id)
            categories = request.vars.categories           
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:            
            return i2p.admin_categories.assign(id,categories)
            
        
    else:
        return json_response(message=T("Problem with the values submitted"),\
                             alert=2,value="")





def user():
    
    if not check_credentials_is_admin():
        return
    
    try:
        subarea = request.args[0]        
    except:
        return json_response(message=T("Problem with the values submitted"),\
                             alert=2,value="")
        
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules
    
    i2p.load_mod_users_admin() #load admin_articles
    
    
    if subarea=="list":
    
        try:
            page = int(request.vars.page)
        except:
            page = 1
        
        try:
            search_text = request.vars.search        
        except:
            search_text = ""  
            
        return i2p.admin_users.list(page,search_text)       
        
            
    elif subarea=="save_firstname":            
        
        try:
            id = int(request.vars.id)
            value = request.vars.value                    
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else: 
            return i2p.admin_users.save_firstname(id,value)       
            
    
    elif subarea=="save_lastname":            
        
        try:
            id = int(request.vars.id)
            value = request.vars.value                    
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else: 
            return i2p.admin_users.save_lastname(id,value)       
             
        
    elif subarea=="save_email":            
        
        try:
            id = int(request.vars.id)
            value = request.vars.value                    
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else: 
            return i2p.admin_users.save_email(id,value)       
            
        
    elif subarea=="get_firstname":            
        
        try:
            id = int(request.vars.id)                                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:  
            return i2p.admin_users.get_firstname(id)      
            
    
    elif subarea=="get_lastname":            
        
        try:
            id = int(request.vars.id)                                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:       
            return i2p.admin_users.get_lastname(id) 
               
        
    elif subarea=="get_email":            
        
        try:
            id = int(request.vars.id)                                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else: 
            return i2p.admin_users.get_email(id)       
                         
            
    elif subarea=="delete":            
        
        try:
            id = int(request.vars.id)        
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:   
            return i2p.admin_users.delete(id)     
            
    
    elif subarea=="activate":            
        
        try:
            id = int(request.vars.id)        
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:        
            return i2p.admin_users.activate(id)
            
    
    elif subarea=="disable":            
        
        try:
            id = int(request.vars.id)        
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:   
            return i2p.admin_users.disable(id)     
            
    
    elif subarea=="block":            
        
        try:
            id = int(request.vars.id)        
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:       
            return i2p.admin_users.block(id) 
            
    
    elif subarea=="change_pass":            
        
        try:
            id = int(request.vars.id)        
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:      
            return i2p.admin_users.change_password(id,value)  
            
        
    elif subarea=="get_pass":            
        
        try:
            id = int(request.vars.id)                                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:        
            return i2p.admin_users.get_password(id)
                   
        
    elif subarea=="set_admin":            
        
        try:
            id = int(request.vars.id)        
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:      
            return i2p.admin_users.setadmin(id)  
                      
            
    else:
        return json_response(message=T("Problem with the values submitted"),\
                             alert=2,value="")






def comment():
    
    if not check_credentials_is_admin():
        return    
    
    try:
        subarea = request.args[0]        
    except:
        return json_response(message=T("This function doesn't exist"),\
                             alert=2,value="")
        
    
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules        
    
    i2p.load_mod_comments_admin()
        
    if subarea=="list":
        try:
            page = int(request.vars.page)        
        except:
            page = 1  
        
        return i2p.admin_comments.list(page)
        
    
    elif subarea=="get":            
        
        try:
            id = int(request.vars.id)                                
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:  
            return i2p.admin_comments.get(id)      
            
        
    elif subarea=="change":            
        
        try:
            id = int(request.vars.id)        
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else: 
            return i2p.admin_comments.change(id,value)       
                               
            
    elif subarea=="delete":
                    
        try:
            id = int(request.vars.id)        
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else: 
            return i2p.admin_comments.delete(id)       
                     
            
    else:
        return json_response(message=T("Problem with the values submitted"),\
                             alert=2,value="")





def cat():

    
    if not check_credentials_is_admin():
        return
            
    try:
        subarea = request.args[0]        
    except:
        return json_response(message=T("This function doesn't exist"),\
                             alert=2,value="")
 
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules
    
    i2p.load_mod_categories_admin()

    
    if subarea=="list":
        try:
            page = int(request.vars.page)        
        except:
            page = 1  
        
        return i2p.admin_categories.list(page)
                
    
    elif subarea=="add":
        
        return i2p.admin_categories.add()
        
    
    elif subarea=="delete":
        
        try:
            id = int(request.vars.id)        
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else: 
            return i2p.admin_categories.delete(id)       
            
        
    elif subarea=="change_title":            
        
        try:
            id = int(request.vars.id)        
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:
            return i2p.admin_categories.change_title(id,value)        
               
        
    
    elif subarea=="get_title":            
        
        try:
            id = int(request.vars.id)           
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:     
            return i2p.admin_categories.get_title(id)   
                        

    elif subarea=="change_name":            
        
        try:
            id = int(request.vars.id)        
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:  
            return i2p.admin_categories.change_name(id,value)      
               
            
    elif subarea=="get_name":            
        
        try:
            id = int(request.vars.id)           
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else: 
            return i2p.admin_categories.get_name(id)       
            
        
        
    elif subarea=="change_description":            
        
        try:
            id = int(request.vars.id)        
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else: 
            return i2p.admin_categories.change_description(id,value)       
               
            
    elif subarea=="get_description":            
        
        try:
            id = int(request.vars.id)           
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:   
            return i2p.admin_categories.get_description(id)     
            
                    
    else:
        return json_response(message=T("Problem with the values submitted"),\
                             alert=2,value="")
    
    
    

def info():
    
    if not check_credentials_is_admin():
        return
    
    try:
        subarea = request.args[0]        
    except:       
        return json_response(message=T("This function doesn't exist"),\
                             alert=2,value="")
    
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules
    
    i2p.load_mod_siteinfo_admin()
    
    
    if subarea=="list":
        return i2p.admin_info.list()
        
    
    elif subarea=="get_title":
        return i2p.admin_info.get_title()
        
    
    elif subarea=="get_subtitle":
        return i2p.admin_info.get_subtitle()
        
    
    elif subarea=="get_description":
        return i2p.admin_info.get_description()
        

    elif subarea=="get_frontpage":
        return i2p.admin_info.get_frontpage()
        
    
    elif subarea=="get_about":
        return i2p.admin_info.get_about()
        
    
    elif subarea=="get_keywords":
        return i2p.admin_info.get_keywords()
        
    
    elif subarea=="get_copyright":
        return i2p.admin_info.get_copyright()
        
    
    elif subarea=="get_logo":
        return i2p.admin_info.get_logo()
        
    
    elif subarea=="save_logo":
        try:
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:        
            return i2p.admin_info.save_logo(value)          
            
    
    elif subarea=="save_title":
        try:
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:        
            return i2p.admin_info.save_title(value)         
        
    
    elif subarea=="save_subtitle":
        try:
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:            
            return i2p.admin_info.save_subtitle(value)            
        
    
    elif subarea=="save_description":
        try:
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:        
            return i2p.admin_info.save_description(value)            
        

    elif subarea=="save_frontpage":
        try:
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:        
            return i2p.admin_info.save_frontpage(value)           
        
    
    elif subarea=="save_about":
        try:
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:        
            return i2p.admin_info.save_about(value)        
        
    
    elif subarea=="save_keywords":
        try:
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:        
            return i2p.admin_info.save_keywords(value)           
        
    
    elif subarea=="save_copyright":
        try:
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:        
            return i2p.admin_info.save_copyright(value)          
                
    else:
        return json_response(message=T("Problem with the values submitted"),\
                             alert=2,value="")
    
    

def image():
    
    if not check_credentials_is_admin():
        return
    
    try:
        subarea = request.args[0]        
    except:
        return json_response(message=T("This function doesn't exist"),\
                             alert=2,value="")
    
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules
    
    i2p.load_mod_images_admin()
    
    if subarea=="list":    
        
        try:
            page = int(request.vars.page)        
        except:
            page = 1 
        
        return i2p.admin_images.list(page)        
        
    
    elif subarea=="delete":
        
        try:
            id = int(request.vars.id)        
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:
            return i2p.admin_images.delete(id)        
        
    
    elif subarea=="form_upload":
        
        return i2p.admin_images.form_upload()
          
    
    elif subarea=="change_comment":            
        
        try:
            id = int(request.vars.id)        
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else: 
            return i2p.admin_images.change_comment(id,value)       
            
        
    elif subarea=="get_comment":            
        
        try:
            id = int(request.vars.id)           
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:     
            return i2p.admin_images.get_comment(id)   
            
                  
    else:
        return json_response(message=T("Problem with the values submitted"),\
                             alert=2,value="")



def links():
    
    if not check_credentials_is_admin():
        return
    
    try:
        subarea = request.args[0]        
    except:
        return json_response(message=T("This function doesn't exist"),\
                             alert=2,value="")
    
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules        
        
    i2p.load_mod_links_admin()
    
    if subarea=="list":    
        
        try:
            page = int(request.vars.page)        
        except:
            page = 1  
        
        return i2p.admin_links.list(page)
        
    
    elif subarea=="add":
        
        return i2p.admin_links.add()
        
    
    
    elif subarea=="change_title":           
        
        try:
            id = int(request.vars.id)        
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:
            return i2p.admin_links.change_title(id,value)        
               
        
    
    elif subarea=="get_title":            
        
        try:
            id = int(request.vars.id)           
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else: 
            return i2p.admin_links.get_title(id)       
            
        
    elif subarea=="change_url":           
        
        try:
            id = int(request.vars.id)        
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:    
            return i2p.admin_links.change_url(id,value)    
                   
    
    elif subarea=="get_url":            
        
        try:
            id = int(request.vars.id)           
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:   
            return i2p.admin_links.get_url(id)     
                        
            
    elif subarea=="change_description":           
        
        try:
            id = int(request.vars.id)        
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:  
            return i2p.admin_links.change_description(id,value)      
                   
    
    elif subarea=="get_description":            
        
        try:
            id = int(request.vars.id)           
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:        
            return i2p.admin_links.get_description(id)
               
        
    elif subarea=="delete":
        
        try:
            id = int(request.vars.id)        
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:    
            return i2p.admin_links.delete(id)    
              

                      
    else:
        return json_response(message=T("Problem with the values submitted"),\
                             alert=2,value="")
        
        
       
def style():
    
    if not check_credentials_is_admin():
        return
    
    try:
        subarea = request.args[0]        
    except:
        return json_response(message=T("This function doesn't exist"),\
                             alert=2,value="")
    
    #begin load all base modules
    i2p.load_mod_common() #load common modules
    i2p.db_definitions() #define tables
    #end load all base modules    
    
    i2p.load_mod_styles_admin()
    
    if subarea=="list":
            
        try:
            page = int(request.vars.page)        
        except:
            page = 1
            
        return i2p.admin_styles.list(page)        
    
    
    elif subarea=="add":
        
        return i2p.admin_styles.add()
        
    
    elif subarea=="change_title":           
        
        try:
            id = int(request.vars.id)        
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:
            return i2p.admin_styles.change_title(id,value)        
                      
    
    elif subarea=="get_title":            
        
        try:
            id = int(request.vars.id)           
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:       
            return i2p.admin_styles.get_title(id) 
            
        
        
    elif subarea=="change_css":           
        
        try:
            id = int(request.vars.id)        
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:     
            return i2p.admin_styles.change_css(id,value)   
               
        
    
    elif subarea=="get_css":            
        
        try:
            id = int(request.vars.id)           
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:  
            return i2p.admin_styles.get_css(id)      
            

    elif subarea=="change_author":           
        
        try:
            id = int(request.vars.id)        
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else: 
            return i2p.admin_styles.change_author(id,value)       
                       
    
    elif subarea=="get_author":            
        
        try:
            id = int(request.vars.id)           
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:        
            return i2p.admin_styles.get_author(id)
            
        
        
    elif subarea=="delete":
        
        try:
            id = int(request.vars.id)        
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:
            return i2p.admin_styles.delete(id)        
            
        
    
    elif subarea=="apply":
        
        try:
            id = int(request.vars.id)        
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:  
            return i2p.admin_styles.apply(id)      
    
    
    elif subarea=="availables":
        
        try:
            id = int(request.vars.id)        
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else:                           
            return i2p.admin_styles.availables(id)
    
    elif subarea=="change_style":           
        
        try:
            id = int(request.vars.id)        
            value = request.vars.value
        except:
            return json_response(message=T("Problem with the values submitted"),\
                                 alert=2,value="")
        else: 
            return i2p.admin_styles.change_style(id,value)      
                     
                  
    else:
        return json_response(message=T("Problem with the values submitted"),\
                             alert=2,value="")



        
