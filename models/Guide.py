# @name    Guide.py
# @author  Samuel A.
# @date    Oct 11 13
# @purpose db model for Guide data


import Root
import Utility
from google.appengine.ext import db


date = ""

class Guide(db.Model, Root.Handler):
    _firstname   = db.StringProperty()
    _lastname    = db.StringProperty()
    _email       = db.EmailProperty()
    _phoneNumber = db.PhoneNumberProperty()
    _dateOfBirth = db.DateProperty()
    _locations   = db.ListProperty(db.Key)
    _workDays    = db.ListProperty(db.Key)
    _picture     = db.BlobProperty()
    _languages   = db.ListProperty(db.Key)
    _rating      = db.ReferenceProperty(Review, collection_name='reviews')


    
    def authenticate(self, p):
        if self.auth_password(p, self._password, self._salt):
            return True
        else:
            return False
    
    
    def following(self):
        return len(self._following)
    
    
    def followers(self):
        return len(self._followers)
    
    
    def add_user(self, name, password, handle):
        user_list = User.all()
        names = [user._username for user in user_list]
        
        if name and password and handle:
            if name in names:
                return None, "%s is already taken" % name
            
            else:
                salt_pass = self.hash_password(password, name)
                new_user = User(_username=name, _password=str(salt_pass[0]), _handle=handle, _salt=str(salt_pass[1]))
                new_user.put()
                return new_user, 'ok'
            
        else:
            return None, "All fields are required"
        
        
    def login(self, username, password):
        user = User.gql('WHERE _username=:1', username).get()
        
        if user:
            if (user.auth_password(password, user._password, user._salt)):
                return user, 'ok'
        else:
            return None, 'error'
        
        
    def follow(self, user_id, f_if):
        user = Users.get_by_id(user_id).followers.append(f_id)

    
    
    
    def total_tweets (self, user_id):
        user = User.get_by_id(user_id)
        count = user.tweets.count()
#        count = Tweet.all(keys_only=True).count()
        return count
        
    def getDate(self, x):
        return x._date
    
    def my_tweets (self, user):
        tweets = db.GqlQuery("SELECT * FROM Tweet WHERE _user=:1 ORDER BY _date DESC", user)
         
        return tweets
    
    
    def wall_tweets (self, user_id):
        user = User.get_by_id(user_id)
        following = user._following
        
        tweets = []
        user_tweets = self.my_tweets(user)
        tweets = list(user_tweets)
        for f in following:
            tweets += list(self.my_tweets(f))
            
        temp = sorted(tweets, key=self.getDate, reverse=True)
        if len(temp) > 0:
            date = temp[0]._date
        return tweets
    
    
    def new_tweet(self, user_id, tweet):
        user = User.get_by_id(user_id)
        Tweet(_user=user, _tweet=tweet).put()
                
                           
    def get_name(self, user):
        return User.get_by_id(user)
    
    @staticmethod
    def get_new_tweets(user_id):
        new_tweets = db.GqlQuery("SELECT * FROM Tweet WHERE _user=:1 AND _date>:2 ORDER BY _date DESC", user_id, date).count()
        return new_tweets




