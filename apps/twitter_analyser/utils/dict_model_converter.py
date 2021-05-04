import collections
import datetime

from apps.twitter_analyser.models import TwitterProfile, Tweet, Hashtag


class DictModelConverter:
    """
    Class DictModelConverter's (static) methods take dictionaries of attributes of model classes and return almost
    complete objects of these classes (built objects don't have objects in relationships for now)
    """

    @staticmethod
    def get_profile_from_dict(profile_dict):
        """
        Method for getting TwitterProfile class objects from dictionaries of its attributes
        :param profile_dict: dictionary of format {'profile_id': int, 'username': str}
        :return: TwitterProfile object with attributes above and a save date which is current time
        """

        return TwitterProfile(profile_id=profile_dict['profile_id'], username=profile_dict['username'],
                              save_date=datetime.datetime.now())

    @staticmethod
    def get_tweet_from_dict(tweet_dict):
        """
        Method for getting Tweet class objects from dictionaries of class's attributes
        :param tweet_dict: dictionary of format {'tweet_id': int, 'creation_date': date, 'text': str,
        'retweets': int, 'likes': int}
        :return: Tweet object with attributes above and a save date which is current time
        """

        return Tweet(tweet_id=tweet_dict['tweet_id'], creation_date=tweet_dict['creation_date'],
                     text=tweet_dict['text'], save_date=datetime.datetime.now(), retweets=tweet_dict['retweets'],
                     likes=tweet_dict['likes'])

    @staticmethod
    def get_tweets_list(tweet_dict_list, how_many):
        """
        Method for getting Tweet class objects' list from list of dictionaries of class's attributes
        :param how_many: how many Tweet object should be in the resulting list as tweet_dict_list doesn't provide unique
        elements
        :param tweet_dict_list: list of dictionaries of format {'tweet_id': int, 'creation_date': date, 'text': str,
        'retweets': int, 'likes': int}
        :return: list of Tweet objects with attributes like in dictionary above and a save date which is current time
        """

        unique_list = []

        for tweet in [DictModelConverter.get_tweet_from_dict(tweet_dict) for tweet_dict in tweet_dict_list]:
            if tweet not in unique_list:
                unique_list.append(tweet)

        return unique_list[:how_many]

    @staticmethod
    def get_hashtag_from_dict(hashtag_dict):
        """
        Method for getting Hashtag class objects from dictionaries of class's attributes
        :param hashtag_dict: dictionary of format {'text': str, 'tweet_volume': int}
        :return: Hashtag object with attributes like in dictionary above and a save date which is current time
        """

        return Hashtag(save_date=datetime.datetime.now(), text=hashtag_dict['text'],
                       tweet_volume=hashtag_dict['tweet_volume'])

    @staticmethod
    def get_hashtag_list(hashtag_dict_list):
        """
        Method for getting Hashtag class objects' list from list of dictionaries of class's attributes
        :param hashtag_dict_list: list of dictionaries of format {'text': str, 'tweet_volume': int}
        :return: list of Hashtag objects with attributes like in dictionary above and a save date which is current time
        """

        return [DictModelConverter.get_hashtag_from_dict(hashtag_dict) for hashtag_dict in hashtag_dict_list]
