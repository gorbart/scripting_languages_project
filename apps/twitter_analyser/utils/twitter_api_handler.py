import tweepy

POLAND_WOEID = 23424923


class TwitterApiHandler:
    """
    Class TwitterApiHandler connects to Twitter API and retrieves from there information requested by project's user.
    Attributes:
        - auth - authorisation object, created with Twitter API key and secret given in __init__
        - api - api connection object, created with auth object
    """

    def __init__(self, key, secret):
        self.auth = tweepy.AppAuthHandler(key, secret)
        self.api = tweepy.API(self.auth)

    def get_trending_hashtags(self, how_many, woeid=POLAND_WOEID):
        """
        Method for getting a list of hashtags for a specific location
        :param how_many: specifies number of retrieved hashtags (may be less as there is 50 trends and not all of them
        are hashtags)
        :param woeid: Yahoo Where On Earth IDentifier indicating geographical location of retrieved trends; default
        value is Poland's WOEID as current project is going to use it frequently
        :return: list of dictionaries with format {'text': hashtags' text, 'volume': number of hashtag's related Tweets
        for specified country}
        """

        return [{'text': trend['name'], 'tweet_volume': trend['tweet_volume']}
                for trend in self.api.trends_place(id=woeid)[0]['trends']
                if trend['name'][0] == '#' and trend['tweet_volume']][:how_many]

    def get_trending_hashtags_for_world(self, how_many):
        """
        Method for getting a list of hashtags for the entire world
        :param how_many: specifies number of retrieved hashtags (may be less as there is 50 trends and not all of them
        are hashtags)
        :return: list of dictionaries with format hashtags' text and number of hashtag's related Tweets for the entire
        world
        """

        return self.get_trending_hashtags(how_many, 1)

    def get_tweets_with_hashtag(self, query, how_many):
        """
        Method for getting a list of Tweets for a given hashtag
        :param query: string query used for searching matching posts - hashtags
        :param how_many: indicates how many Tweets should be iterated over
        :return: list of dictionaries with tweet's id, its creation date, text and numbers of retweets and likes, which
        is 5 times bigger than how_many as some tweets may be retweets of each other
        """

        return [{'tweet_id': str(tweet.id), 'creation_date': tweet.created_at,
                 'text': tweet.full_text if not hasattr(tweet, 'retweeted_status')
                 else tweet.retweeted_status.full_text,
                 'retweets': tweet.retweet_count, 'likes': tweet.favorite_count} for tweet in
                tweepy.Cursor(self.api.search, q=query, tweet_mode="extended").items(how_many * 5)]

    def get_tweets_for_author(self, author, how_many):
        """
        Method for getting a list of Tweets posted by given user
        :param author: query used for searching matching posts - author's username
        :param how_many: indicates how many Tweets should be iterated over
        :return: list of dictionaries with tweet's id, its creation date, text and numbers of retweets and likes
        """

        return [{'tweet_id': str(tweet.id), 'creation_date': tweet.created_at,
                 'text': tweet.text, 'retweets': tweet.retweet_count, 'likes': tweet.favorite_count}
                for tweet in tweepy.Cursor(self.api.user_timeline, id=author).items(how_many)]

    def get_profile(self, query):
        """
        Method for getting specified Twitter's profile
        :param query: profile's username or id
        :return: dictionary of username and id of the most matching profile
        """

        if isinstance(query, str):
            profile = self.api.lookup_users(screen_name=query)[0]
        else:
            profile = self.api.lookup_users(user_id=query)[0]
        return {'profile_id': str(profile.id), 'username': profile.screen_name}
