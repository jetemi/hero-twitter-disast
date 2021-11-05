TRACK_WORDS = ['Disaster', 'fire']
TABLE_NAME = "Disaster"         #Change DATE,integer, double precision(PostGreSQL) DATETIME,int, double(mySQL)
TABLE_ATTRIBUTES = "id_str VARCHAR(255), created_at DATE, text VARCHAR(255), \
            polarity integer, subjectivity integer, user_created_at VARCHAR(255), user_location VARCHAR(255), \
            user_description VARCHAR(255), user_followers_count integer, longitude double precision, latitude double precision, \
            retweet_count integer, favorite_count integer"