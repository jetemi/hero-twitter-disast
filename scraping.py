# This is Main function.
# Extracting streaming do ata from Twitter, pre-processing, and loading intMySQL
from config import settings
import dbsettings # Import related setting constants from settings.py 
import os
import psycopg2
import re
import tweepy
import pandas as pd
from textblob import TextBlob
# Streaming With Tweepy 
# http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html#streaming-with-tweepy


# Override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    '''
    Tweets are known as “status updates”. So the Status class in tweepy has properties describing the tweet.
    https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html
    '''
    
    def on_status(self, status):
        '''
        Extract info from tweets
        '''
        
        if status.retweeted:
            # Avoid retweeted info, and only original tweets will be received
            return True
        # Extract attributes from each tweet
        id_str = status.id_str
        created_at = status.created_at
        text = deEmojify(status.text)    # Pre-processing the text  
        sentiment = TextBlob(text).sentiment
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity
        
        user_created_at = status.user.created_at
        user_location = deEmojify(status.user.location)
        user_description = deEmojify(status.user.description)
        user_followers_count =status.user.followers_count
        longitude = None
        latitude = None
        if status.coordinates:
            longitude = status.coordinates['coordinates'][0]
            latitude = status.coordinates['coordinates'][1]
            
        retweet_count = status.retweet_count
        favorite_count = status.favorite_count

        
        # Store all data in Heroku PostgreSQL
        cur = conn.cursor()
        sql = "INSERT INTO {} (id_str, created_at, text, polarity, subjectivity, user_created_at, user_location, user_description, user_followers_count, longitude, latitude, retweet_count, favorite_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(dbsettings.TABLE_NAME)
        val = (id_str, created_at, text, polarity, subjectivity, user_created_at, user_location, \
            user_description, user_followers_count, longitude, latitude, retweet_count, favorite_count)
        cur.execute(sql, val)
        conn.commit()
        
        delete_query = '''
        DELETE FROM {0}
        WHERE id_str IN (
            SELECT id_str 
            FROM {0}
            ORDER BY created_at asc
            LIMIT 200) AND (SELECT COUNT(*) FROM Disaster) > 9600;
        '''.format(dbsettings.TABLE_NAME)
        
        cur.execute(delete_query)
        conn.commit()
        cur.close()
    
    
    def on_error(self, status_code):
        '''
        Since Twitter API has rate limits, stop srcraping data as it exceed to the thresold.
        '''
        if status_code == 420:
            # return False to disconnect the stream
            return False

def clean_tweet(self, tweet): 
    ''' 
    Use sumple regex statemnents to clean tweet text by removing links and special characters
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) \
                                |(\w+:\/\/\S+)", " ", tweet).split()) 
def deEmojify(text):
    '''
    Strip all non-ASCII characters to remove emoji characters
    '''
    if text:
        return text.encode('ascii', 'ignore').decode('ascii')
    else:
        return None


DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

'''
Check if this table exits. If not, then create a new one.
'''
'''
cur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{}'
        """.format(dbsettings.TABLE_NAME))
if cur.fetchone()[0] != 1:
    cur.execute("CREATE TABLE {} ({});".format(dbsettings.TABLE_NAME, dbsettings.TABLE_ATTRIBUTES))
    cur.execute("CREATE TABLE {} ({});".format(dbsettings.BACKUP, dbsettings.BACKUP_ATTRIBUTES))
    conn.commit()
'''    
cur.close()


auth  = tweepy.OAuthHandler(settings.api_key, settings.api_secret_key)
auth.set_access_token(settings.access_token, settings.access_token_secret)
api = tweepy.API(auth)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)
myStream.filter(languages=["en"], track = dbsettings.TRACK_WORDS)
# However, this won't be reached as the stream listener won't stop automatically
# Press STOP button to finish the process.
conn.close()