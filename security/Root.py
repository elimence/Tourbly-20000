# @name    Root.py
# @author  Samuel A.
# @date    Oct 13 13
# @purpose assorted features, read code docs below


import os
import cgi
import hmac
import random
import string
import jinja2
import webapp2
import datetime

    
## Globals

ph           = 'squemishossifragealladinandthemagiclampallinanutshellTheEndIsNighAndAllMustPrepare'
template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env    = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)





## => Implements various utility functions for handling security operations

class Security():

    # Name - Hash_string
    # Desc
    #   Makes a hash of any string using a secret key
    # params
    #   self  : Ref    -> reference to object instance
    #   ref   : String -> value to be hashed
    # returns
    #   : String -> hashed version of string ref

    def Hash_string(self, ref):
        cypher = hmac.new(ph, str(ref))
        return cypher.hexdigest()
    

    # Name - hash_password
    # Desc
    #   encrypts passwords by hashing with a uniquely generated salt
    #   combined with the secret key
    # params
    #   self  : Ref    -> reference to object instance
    #   _args : Object :: name     : String  -> name of user (used to generate unique salt)
    #                  :: password : String  -> password to be encrypted
    # returns
    #   :String -> hashed password and random salt

    def hash_password(self, _args):
        salt = self.rand_salt(_args.name)
        hash_pass = hmac.new(salt+ph, str(_args.password))
        return hash_pass.hexdigest(), salt
        

    # Name - auth_password
    # Desc
    #   verifies passwords by hashing and comparing with stored hash
    # params
    #   self  : Ref    -> reference to object instance
    #   _args : Object :: salt       : String  -> stored salt
    #                  :: plainPass  : String  -> password to be verified
    #                  :: hashedPass : String  -> stored hash of password
    # returns
    #   : Boolean -> True if matched, False otherwise
        
    def auth_password(self, _args):
        if hmac.new(salt+ph, str(p)).hexdigest() == h:
            return True
        else:
            return False



    # Name - auth_hash
    # Desc
    #   compares plain string to hash for possible match (used to check for tamparing)
    # params
    #   self  : Ref    -> reference to object instance
    #   _args : Object :: plainStr  : String  -> plain text to be verified
    #                  :: hashedStr : String  -> hashed string for integrity check
    # returns
    #   : Boolean -> True if matched, False otherwise

    def auth_hash(self, plain, cypher):
        if cypher == self.Hash_string(plain):
            return True
        else:
            return False
        


    # Name - rand_salt
    # Desc
    #   generates a random salt using a given string as base
    # params
    #   self  : Ref    -> reference to object instance
    #   _args : Object :: base  : String  -> base string used to generate salt
    # returns
    #   : String -> the generated salt

    def rand_salt(self, _args):
        return ''.join(random.choice(_args.base) for i in range(8)) 
        + ''.join(random.choice(string.letters) for i in range(8))







# => Request handler extended with class Security and misc functionality

class Handler(Security, webapp2.RequestHandler):
    def w(cls,*a, **kw):
        Handler.response.out.write(*a, **kw)
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
        
    # standard render function
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
             


    # Name - set_cookie
    # Desc
    #   Sets a cookie given the name and value
    # params
    #   self  : Ref    -> reference to object instance
    #   _args : object :: name       : String  -> name of cookie
    #                  :: value      : String  -> contents of cookie
    #                  :: [validity] : Integer -> validity period of cookie default=4wks
    # returns
    #   : Void -> returns nothing

    def set_cookie(self, _args):
        self.response.headers.add_header('Set-Cookie', '%s=%s|%s; expires=%s' % 
             (str(_args.name), str(_args.value), self.Hash_string(_args.value), 
              (datetime.datetime.now()
              + datetime.timedelta(weeks=_args.validity | 4)).strftime('%a, %d %b %Y %H:%M:%S GMT')))
        


    # Name - logout
    # Desc
    #   Closes the current session by clearing login cookies
    # params
    #   self        : Ref    -> reference to object instance
    #   cookie_list : List   -> list of cookies to be unset
    # returns
    #   : Void -> returns nothing

    def logout(self, cookie_list):
        for cookie in cookie_list:
            self.response.headers.add_header('Set_Cookie', '%s=' %(cookie))


    # Name - get_cookie
    # Desc
    #   retrieves the value of a given cookie
    # params
    #   self        : Ref    -> reference to object instance
    #   name  : String -> name of cookie to be retrieved
    # returns
    #   : List -> list containing a plain text cookie and it's hash or [None, None] if not found

    def get_cookie(self, name):
        cookie = self.request.cookies.get(name, None)
        
        if cookie:
            temp = cookie.split('|')
            return temp
        else:
            return [None, None]
    


    # Name - get_cookie ==> (Deprecated)
    # Desc
    #   retrieves the value of a given cookie
    # params
    #   self : Ref    -> reference to object instance
    #   name : String -> name of cookie to be retrieved
    # returns
    #   : 

    def get_user_id(self):
        cookie = self.request.cookies.get('id', None)
        return int(cookie.split('|')[0])
    


    # Name - create_session
    # Desc
    #   creates a user session by setting appropriate cookies
    # params
    #   self         : Ref  -> reference to object instance
    #   session_vars : List -> list of objects with cookie name and value as follows
    #                           :: name  -> name of cookie
    #                           :: value -> value of cookie
    # returns
    #   : Void -> returns nothing

    def create_session(self, session_vars):
        for cookie in session_vars:
            self.set_cookie(cookie.name, cookie.value)
        
        

    # Name - check_session
    # Desc
    #   verifies client's login status
    # params
    #   self           : Ref    -> reference to object instance
    #   session_cookie : String -> name of session cookie
    # returns
    #   : Boolean -> True if user is logged in, False otherwise

    def check_session(self, session_cookie):
        session = self.get_cookie(session_cookie)
        return self.auth_hash(session[0], session[1])
        
        