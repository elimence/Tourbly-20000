# @name    Review.py
# @author  Samuel A.
# @date    Oct 13 13
# @purpose db model for Review data


import Root
from google.appengine.ext import db

date = ""

class Review(db.Model, Root.Handler):
    _reviewer = db.StringProperty()
    _reviewee = db.StringProperty()
    _rating   = db.IntegerProperty()
    _comment  = db.StringProperty()

class User(db.Model, Root.Handler):
    _username = db.StringProperty()
    _password = db.StringProperty()
    _handle = db.StringProperty()
    _salt = db.StringProperty()
    _created = db.DateTimeProperty(auto_now_add = True)
    
    _followers = db.ListProperty(db.Key)
    _following = db.ListProperty(db.Key)
    
    
    def auth_user(self, p):
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

    
    
    
    
class Tweet(db.Model):
    _user = db.ReferenceProperty(User, collection_name='tweets')
    _tweet = db.TextProperty()
    _date = db.DateTimeProperty(auto_now_add = True)
    _last = db.DateTimeProperty()
    
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




