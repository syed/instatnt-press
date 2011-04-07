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
from gluon.tools import *

#local
from utils import *

POST_PUBLISHED = 1
POST_IS_PAGE = 1
POST_IS_NOT_PAGE = 0


class FillData(object): 
    
    
    def __init__(self, i2p):
        
        self.i2p = i2p        
            


    def _new_user(self, first_name, last_name, email, passw):    
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        auth = self.i2p.environment.auth
        
        users = db(db.auth_user.email==email).select()
        if users:
            return users[0].id
        else:
            my_crypt = CRYPT(key=auth.settings.hmac_key)
            crypt_pass = my_crypt(passw)[0]        
            id_user= db.auth_user.insert(
                                       first_name=first_name,
                                       last_name=last_name,
                                       email = email,
                                       password = crypt_pass                             
                                       )
            return id_user
        
        
    #Blog information: fill default values if not exist
    def _info_site(self, site_title, \
                        site_subtitle, site_description, \
                        site_aboutme, site_keywords, \
                        site_footer, site_front):
        
        db = self.i2p.db
                
        siteinfo = db(db.siteinfo.id>0).select() 
        if siteinfo:
            return siteinfo[0].id
        else:
            #create it   
            id_info= db.siteinfo.insert(
                                       site_title=site_title,
                                       site_subtitle=site_subtitle,
                                       site_description=site_description,
                                       site_aboutme=site_aboutme,
                                       site_keywords=site_keywords,
                                       site_footer=site_footer,
                                       site_front=site_front,
                                       site_language="en"
                                       )
            return id_info   




    def info_default(self):
        
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        
        img_python = IMG(_src=URL(r=request,c='static',f='images/powered-python.png'), \
                         _alt='Logo python', _style='margin-left: 10px;', \
                         _title='%s'%T('Powered by python'))
        img_web2py = IMG(_src=URL(r=request,c='static',f='images/poweredby.png'), \
                         _alt='Logo web2py', _style='margin-left: 0px; padding: 4px;', \
                         _title='%s'%T('Powered by Web2py Enterprise Framework'))
        img_instant = IMG(_src=URL(r=request,c='static',f='images/powered-instant.png'), \
                          _alt='Logo instant press', _style='margin-left: 10px;', \
                          _title='%s'%T('Powered by Instant Press'))
        link_python = A(img_python,_href="http://www.python.com",_title="Python main site")
        link_web2py = A(img_web2py,_href="http://www.web2py.com", _title="Web2py main site")
        link_instant = A(img_instant,_href="http://www.instant2press.com", _title="Instant2press site")
            
        site_title='Instant Press'
        site_subtitle='Instant Press'
        site_description='''Instant Press is a CMS developed in Web2py Enterprise Framework. Instant Press is <strong>simple, easy to use and attractive.</strong>
                            Upload to your web2py framework or to Google Application Engine and you are ready to start!.''' 
        site_front='''<h1>Welcome to Instant Press</h1> <br /> <strong>Instant Press</strong> is a CMS developed in Web2py Framework. Instant Press is <strong>simple, easy to use and attractive.</strong>
                            Upload to your web2py framework or to Google Application Engine and you are ready to start!.
                            <p>Change this with 'change front page' in admin panel.</p>                                                                       
                            <ul>                       
                            <li><strong>Installation Notes</strong>
                                <ul>
                                    <li>Upload & install packed application (web2py framework)</li>                                
                                    <li>Sign in as: 
                                        <ul>
                                            <li>User: <strong>%(user)s</strong></li>
                                            <li>Password: <strong>%(pass)s</strong></li>                                    
                                        </ul>                                
                                    </li>
                                    <li>Start to customize the site</li>
                                </ul>                        
                            </li>                                                
                            </ul>
                           ''' % {'user': self.i2p.config.email , 'pass': self.i2p.config.passw}
        site_aboutme='''<strong>Instant Press</strong> is a CMS developed in Web2py Enterprise Framework. Instant Press is <strong>simple, easy to use and attractive.</strong>
                            Upload to your web2py framework or to Google Application Engine and you are ready to start!.'''                                   
        site_keywords = 'Instant Press, Python, Web2py, Blog, CMS, Appengine, CKeditor, GAE'                               
        site_footer = '''<div style="padding: 10px;"><strong>Instant Press</strong> by Martin Mulone (C) 2010 - GPL v2.0 License <br />        
        This site is optimized for 1024x768+ screen resolution. <br />      
        %(web2py)s  </div>''' % {'web2py': link_web2py.xml()}  
            
        
        self._info_site(site_title,site_subtitle,\
                             site_description,site_aboutme,\
                             site_keywords,site_footer,site_front)             




    def _require_admin_group(self):  
                
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
          
        group_admin = db(db.auth_group.role==self.i2p.config.group_admin).select()
        if group_admin:
            return group_admin[0].id
        else:       
            id_group_admin = db.auth_group.insert(
                                        role=self.i2p.config.group_admin,
                                        description = 'This is admin group'
                                        )
            return id_group_admin
        
        
        
    
    def _is_no_user_in_db(self):  
        
        db = self.i2p.db
                      
        users_count = db(db.auth_user.id>0).count() 
        if (users_count>0):            
            return False
        
        else:
            return True
    
    
    

    def required_admin(self):
        
        
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        auth = self.i2p.environment.auth
        
        if request.env.web2py_runtime_gae:
            #on gae do nothing
            pass
        else: 
            id_group_admin = self._require_admin_group()    
            users_count = db(db.auth_user.id>0).count() 
            if (users_count==0): #if no users
                id_user = self._new_user(self.i2p.config.first_name,\
                                              self.i2p.config.last_name,\
                                              self.i2p.config.email,\
                                              self.i2p.config.passw)
                auth.add_membership(id_group_admin, id_user) 

 
    
    
    
    def _get_admin_guy(self):
        
        db = self.i2p.db
                
        users = db(db.auth_user.email==self.i2p.config.email).select()
        if users:
            return users[0].id
        else:
            return 0
        

   
    def test_users(self):
        
        
        iduser = self._new_user('Chris','Mills','chris@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills2','chris1@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills3','chris2@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills4','chris3@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills5','chris4@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills6','chris5@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills7','chris6@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills8','chris7@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills9','chris8@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills10','chris9@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills11','chris10@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills12','chris11@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills13','chris12@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills14','chris13@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills15','chris14@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills16','chris15@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills17','chris16@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills18','chris17@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills19','chris18@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills20','chris19@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills21','chris20@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills22','chris21@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills23','chris22@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills24','chris23@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills25','chris24@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills26','chris25@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills27','chris26@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills28','chris27@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills29','chris28@nobody.com','somepasswordhere')
        iduser = self._new_user('Chris','Mills30','chris29@nobody.com','somepasswordhere') 
        
        
        

    def _new_article(self, title, description, \
                          text_slice, published, is_page, name=""):
        
        db = self.i2p.db
        
        id_post = db.posts.insert(title = title,
                                 name = name,
                                 description = description,
                                 text_slice = text_slice,                             
                                 published = published,
                                 is_page = is_page)
        
        return id_post



    def _apply_default_style(self):
        
        db = self.i2p.db
                               
        css = self.i2p.siteinfo._get_css()
        if css=="":
            default_css = self.i2p.siteinfo._get_default_style()
            siteinfo = db(db.siteinfo.id>0).select() 
            if siteinfo:
                info = siteinfo[0]                     
                info.update_record(site_css = default_css,
                                   site_layout = "default")
                                                       


    def default_style(self):
        
                
        db = self.i2p.db
        T = self.i2p.environment.T
        request = self.i2p.environment.request
        
        
        styles = db(db.style.id>0).select()    
        if not styles:
            layout = "default"
            css = self.i2p.siteinfo._get_default_style() #get from file                           
            title = "default style"
            name = layout
            author = "Martin Mulone"
            layout = layout            
            idstyle = db.style.insert(title = title, name = name, \
                                      author = author, css = css, \
                                      layout = layout)                            
                   
            self._apply_default_style() #finally apply the default style
            
            return idstyle

      

    def test_articles(self):
        
        db = self.i2p.db
        
        postscount = db(db.posts.id>0).count()
        if postscount <=0:                
            published = POST_PUBLISHED
            is_page = POST_IS_NOT_PAGE                
            title = 'Test article'
            name = 'test-article'
            
            text_slice = '''
            <h1>Title 01 Heading</h1>
          <hr />
          <h3>Level 03 Heading</h3>
          <p>Lorem ipsum <em>emphasised text</em> dolor sit amet, <strong>strong text</strong> 
          consectetur adipisicing elit, <abbr title="">abbreviated text</abbr> sed do eiusmod tempor 
           incididunt ut labore et dolore magna aliqua. Ut 
          <q>quoted text</q> enim ad minim veniam, quis nostrud exercitation <a href="/">link text</a> 
          ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute 
          <ins>inserted text</ins> irure dolor in reprehenderit in voluptate velit esse cillum 
          dolore eu fugiat nulla pariatur. Excepteur sint occaecat <code>code text</code> cupidatat 
          non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
    
          <p>
          Suspendisse rhoncus, est ac sollicitudin viverra, leo orci sagittis massa, sed condimentum <acronym title="">acronym text</acronym> est tortor a lectus. Curabitur porta feugiat ullamcorper. Integer lacinia mi id odio faucibus eget tincidunt nisl iaculis. Nam adipiscing hendrerit turpis, et porttitor felis sollicitudin et. Donec dictum massa ac neque accumsan tempor. Cras aliquam, ipsum sit amet laoreet hendrerit, purus <del>deleted text</del> sapien convallis dui, et porta leo ipsum ac nunc. Nullam ornare porta dui ac semper. Cras aliquam laoreet hendrerit. Quisque vulputate dolor eget mi porta vel porta nisl pretium. Vivamus non leo magna, quis imperdiet risus. Morbi tempor risus placerat tellus imperdiet fringilla. 
          </p>
    
          <blockquote>
          <p>I am not one who was born in the possession of knowledge; I am one who is fond of antiquity, and earnest in seeking it there.</p>
          </blockquote>
    
          <p><cite><a href="/">Confucius, The Confucian Analects</a></cite>,  (551 BC - 479 BC)</p>
    
          <h3>Level 03 Heading</h3>
    
          <p>Extended paragraph. <a href="">Lorem ipsum</a> dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
          tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud 
          exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in 
          reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint 
          occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
    
          <ol>
          <li>Unus</li>
          <li>Duo</li>
          <li>Tres</li>
          <li>Quattuor</li>
          </ol>
    
          <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla 
          pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit 
          anim id est laborum.</p>
    
          <h3>Header 3</h3>
    
          <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt 
          ut labore et dolore magna aliqua.</p>
    
           <h4>Unordered lists</h4>
                <ul>
                  <li>Lorem ipsum dolor sit amet</li>
                  <li>Consectetur adipisicing elit</li>
                  <li>Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua</li>
                  <li>Ut enim ad minim veniam</li>
                </ul>
          <p>Lorem ipsum dolor sit amet,consectetur adipisicing elit, sed do eiusmod tempor incididunt 
          ut labore et dolore magna aliqua.</p>
    
          <pre><code>body { font:0.8125em/1.618 Arial, sans-serif; 
          background-color:#fff;  
          color:#111;
          }</code></pre>
    
          <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla 
          pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit 
          anim id est laborum.</p>
    
          <h4>Header 4</h4>
    
          <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt 
          ut labore et dolore magna aliqua.</p>
    
          <dl>
          <dt>Definition list</dt>
          <dd>Consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna 
          aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea 
          commodo consequat.</dd>
          <dt>Lorem ipsum dolor sit amet</dt>
          <dd>Consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna 
          aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea 
          commodo consequat.</dd>
    
          </dl>
    
          <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt 
          ut labore et dolore magna aliqua.</p>
          <h4>Ordered list</h4>
          <ol>
                                      <li>List item</li>
                                      <li>List item</li>
                                      <li>List item
                                          <ol>
                                              <li>List item level 2</li>
                                              <li>List item level 2
                                                  <ol>
                                                      <li>List item level 3</li>
                                                      <li>List item level 3</li>
                                                  </ol>
                                              </li>
                                          </ol>
                                      </li>
                                  </ol>                        
                                  <h4>Unordered list</h4>
                                  <ul>
                                      <li>List item 01</li>
                                      <li>List item 02</li>
                                      <li>List item 03
                                          <ul>
                                              <li>List item level 2</li>
                                              <li>List item level 2
                                                  <ul>
                                                      <li>List item level 3</li>
                                                      <li>List item level 3</li>
                                                  </ul>
                                              </li>
    
                                          </ul>
                                      </li>
                                  </ul>
    
          <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt 
          ut labore et dolore magna aliqua.</p>
    
    
               <h4>Tables</h4>
                <table summary="Jimi Hendrix albums">
                <caption>Jimi Hendrix - albums</caption>
                <thead>
                  <tr>
                    <th>Album</th>
                    <th>Year</th>
                    <th>Price</th>
                  </tr>
                  </thead>
                        <tfoot>
                  <tr>
                    <td>Album</td>
                    <td>Year</td>
                    <td>Price</td>
                  </tr>
                  </tfoot>
                  <tbody>
                  <tr>
                    <td>Are You Experienced </td>
                    <td>1967</td>
                    <td>$10.00</td>
                  </tr>
                  <tr>
                    <td>Axis: Bold as Love</td>
                    <td>1967</td>
                    <td>$12.00</td>
                  </tr>
                   <tr>
                    <td>Electric Ladyland</td>
                    <td>1968</td>
                    <td>$10.00</td>
                  </tr>
                  <tr>
                    <td>Band of Gypsys</td>
                    <td>1970</td>
                    <td>$12.00</td>
                  </tr>
                          <tbody>
                </table>
                <p>
          I am <a href="http://devkick.com/lab/tripoli/sample.php?abc123">the a tag</a> example<br>
    
          I am <abbr title="test">the abbr tag</abbr> example<br>
    
          I am <acronym>the acronym tag</acronym> example<br>
          I am <b>the b tag</b> example<br>
          I am <big>the big tag</big> example<br>
    
          I am <cite>the cite tag</cite> example<br>
    
          I am <code>the code tag</code> example<br>
          I am <del>the del tag</del> example<br>
          I am <dfn>the dfn tag</dfn> example<br>
    
          I am <em>the em tag</em> example<br>
    
          I am <font face="verdana">the font tag</font> example<br>
          I am <i>the i tag</i> example<br>
          I am <ins>the ins tag</ins> example<br>
    
          I am <kbd>the kbd tag</kbd> example<br>
    
          I am <q>the q tag <q>inside</q> a q tag</q> example<br>
          I am <s>the s tag</s> example<br>
          I am <samp>the samp tag</samp> example<br>
    
          I am <small>the small tag</small> example<br>
          I am <span>the span tag</span> example<br>
          I am <strike>the strike tag</strike> example<br>
          I am <strong>the strong tag</strong> example<br>
    
          I am <sub>the sub tag</sub> example<br>
          I am <sup>the sup tag</sup> example<br>
          I am <tt>the tt tag</tt> example<br>
          I am <var>the var tag</var> example<br>
    
          I am <u>the u tag</u> example
          </p>
          
          <p>This is a &lt;p&gt; with some <code>code</code> inside.</p>
          
          <h3>What is Lorem Ipsum?</h3>
          <p><b>Lorem Ipsum</b> is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
    
          <p><strong>This</strong> Lorem Ipsum HTML example is created from the parts of Placeholder Markup with Lorem Ipsum - Jon Tan,
          Emastic CSS Framework,
          Tripoli CSS Framework and 
          Baseline CSS Framework .</p>
    
          <address>Address: somewhere, World</address>
          
    
          
         <p>
            <a href="#">Link</a><br>
            <strong>&lt;strong&gt;</strong><br>
            <del>&lt;del&gt; deleted</del><br>
            <dfn>&lt;dfn&gt; dfn</dfn><br>
            <em>&lt;em&gt; emphasis</em>
          </p>
    <pre>
    <code>&lt;html&gt;</code>
        <code>&lt;head&gt;</code>
        <code>&lt;/head&gt;</code>
        <code>&lt;body&gt;</code>
        <code>&lt;div class = "main"&gt; &lt;div&gt;</code>
        <code>&lt;/body&gt;</code>
    <code>&lt;/html&gt; </code>
    </pre>
    
          <tt>&lt;tt&gt;
         Pellentesque tempor, dui ut ultrices viverra, neque urna blandit nisi, id accumsan dolor est vitae risus.
          </tt>
    
        <hr>
        
    
    
        <!-- this following markup from http://bluetrip.org/ -->
        <dl>
          <dt>Description list title 01</dt>
    
          <dd>Description list description 01</dd>
          <dt>Description list title 02</dt>
          <dd>Description list description 02</dd>
          <dd>Description list description 03</dd>
    
        </dl>
        <table>
          <caption>Table Caption</caption>
    
          <thead>
            <tr>
              <th>Table head th</th>
              <td>Table head td</td>
            </tr>
    
          </thead>
          <tfoot>
            <tr>
    
              <th>Table foot th</th>
              <td>Table foot td</td>
            </tr>
          </tfoot>
    
          <tbody>
            <tr>
              <th>Table body th</th>
    
              <td>Table body td</td>
            </tr>
            <tr>
              <td>Table body td</td>
    
              <td>Table body td</td>
            </tr>
          </tbody>
    
        </table>
        
        <hr>
        
        <form action="#">
          <fieldset>
            <legend>Form legend</legend>
    
            <div><label for="f1">Text input:</label><input type="text" id="f1" value="input text" /></div>
            <div><label for="pw">Password input:</label><input type="password" id="pw" value="password" /></div>
            <div><label for="f2">Radio input:</label><input type="radio" id="f2" /></div>
    
            <div><label for="f3">Checkbox input:</label><input type="checkbox" id="f3" /></div>
            <div><label for="f4">Select field:</label><select id="f4"><option>Option 01</option><option>Option 02</option></select></div>
    
            <div><label for="f5">Textarea:</label><textarea id="f5" cols="30" rows="5" >Textarea text</textarea></div>
            <div><label for="f6">Input Button:</label> <input type="button" id="f6" value="button text" /></div>
           
          </fieldset>
    
        </form>        
            '''   
            description = text_slice
            
            self._new_article(title,description,text_slice,published,is_page,name)
