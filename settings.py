TRACK_WORDS = ['Disaster', 'COVID-19', 'Ebola', 'Flu', 'outbreaks', 'thunderstorms', 'avalanche', 'severe weather', 'cold wave', 'heatwave', 'snowstorm', 'sandstorm', 'haze', 'risks', 'hazards', 'crisis', 'emergencies', 'bushfire', 'hurricanes', 'fire', 'storms', 'cyclone', 'landslide', 'flood', 'earthquakes', 'wildfire' 'tornadoes', 'drought', 'tsunamis', 'volcanoes', 'blizzard']
TABLE_NAME = "Disaster"         #Change DATE,integer, double precision(PostGreSQL) DATETIME,int, double(mySQL)
TABLE_ATTRIBUTES = "id_str VARCHAR(255), created_at DATE, text VARCHAR(255), \
            polarity integer, subjectivity integer, user_created_at VARCHAR(255), user_location VARCHAR(255), \
            user_description VARCHAR(255), user_followers_count integer, longitude double precision, latitude double precision, \
            retweet_count integer, favorite_count integer"
BACKUP = "Back_up"
BACKUP_ATTRIBUTES = "daily_user_num integer, daily_tweets_num integer, impressions integer"