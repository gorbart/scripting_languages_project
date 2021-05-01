import credentials
from apps.twitter_analyser.utils.dict_model_converter import DictModelConverter
from apps.twitter_analyser.utils.twitter_api_handler import TwitterApiHandler


class TwitterApiPipeline:
    """
    TwitterApiPipeline class is created to make getting Twitter-related objects easier so that they can be ready to use
    just after get requests.
    Attributes:
        api_handler - TwitterApiHandler class instance, created for use of getting models from Twitter API with
        generated key and secret
    """

    def __init__(self, api_key=credentials.TWITTER_KEY, api_secret=credentials.TWITTER_SECRET):
        self.api_handler = TwitterApiHandler(api_key, api_secret)

    def get_top_hashtags_worldwide(self, how_many=10):
        """
        Method for getting trending in the entire world hashtag object instances straight from Twitter API
        :param how_many: specifies number of retrieved hashtags (may be less as there is 50 trends and not all of them
        are hashtags)
        :return: list of Hashtag objects
        """

        hashtag_dicts = self.api_handler.get_trending_hashtags_for_world(how_many)
        return DictModelConverter.get_hashtag_list(hashtag_dicts)

    def get_recent_tweets_for_hashtag(self, hashtag, how_many=10):
        """
        Method for getting most recent and popular tweets with specified hashtag
        :param hashtag: string query used for searching matching posts - hashtags
        :param how_many: specifies number of retrieved Tweets
        :return: list of Tweet objects
        """

        tweet_dicts = self.api_handler.get_tweets_with_hashtag(hashtag, how_many)
        return DictModelConverter.get_tweets_list(tweet_dicts)

    def get_recent_tweets_for_author(self, author, how_many=10):
        """
        Method for getting most recent and popular tweets posted by user with specified username or id
        :param author: string query used for searching matching posts - author profile's username or id
        :param how_many: specifies number of retrieved Tweets
        :return: list of Tweet objects
        """

        tweet_dicts = self.api_handler.get_tweets_for_author(author, how_many)
        return DictModelConverter.get_tweets_list(tweet_dicts)

    def get_twitter_profile(self, query):
        """
        Method for getting Twitter user Profile by his username or id
        :param query: string query used for searching matching Profile - username or id
        :return: list of Profile objects
        """

        profile_dict = self.api_handler.get_profile(query)
        return DictModelConverter.get_profile_from_dict(profile_dict)
