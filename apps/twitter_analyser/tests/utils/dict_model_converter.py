import datetime

from django.test import SimpleTestCase

from apps.twitter_analyser.models import TwitterProfile, Tweet, Hashtag
from apps.twitter_analyser.utils.dict_model_converter import DictModelConverter


class DictModelConverterTest(SimpleTestCase):

    def test_returns_profile(self):
        profile_dict = {'profile_id': 2, 'username': 'user'}

        prof = TwitterProfile(profile_id=2, username='user')

        prof_test = DictModelConverter.get_profile_from_dict(profile_dict)

        self.assertEqual(prof, prof_test)

    def test_returns_tweet(self):
        date = datetime.datetime.now().date()
        tweet_dict = {'tweet_id': 1, 'creation_date': date, 'text': 'text', 'retweets': 1,
                      'likes': 1}

        tweet = Tweet(tweet_id=1, creation_date=date, text='text', save_date=datetime.datetime.now(), retweets=1,
                      likes=1)

        tweet_test = DictModelConverter.get_tweet_from_dict(tweet_dict)

        self.assertEqual(tweet, tweet_test)

    def test_returns_tweet_list(self):
        date = datetime.datetime.now().date()
        tweet_dict1 = {'tweet_id': 1, 'creation_date': date, 'text': 'text', 'retweets': 1,
                       'likes': 1}
        tweet_dict2 = {'tweet_id': 2, 'creation_date': date, 'text': 'text', 'retweets': 1,
                       'likes': 1}

        tweet1 = Tweet(tweet_id=1, creation_date=date, text='text', save_date=datetime.datetime.now(), retweets=1,
                       likes=1)

        tweet2 = Tweet(tweet_id=2, creation_date=date, text='text', save_date=datetime.datetime.now(), retweets=1,
                       likes=1)

        tweet_test_list = DictModelConverter.get_tweets_list([tweet_dict1, tweet_dict2])

        self.assertEqual([tweet1, tweet2], tweet_test_list)

    def test_returns_hashtag(self):
        hashtag_dict = {'text': '#text', 'tweet_volume': 1}

        hashtag = Hashtag(text='#text', tweet_volume=1)

        hashtag_test = DictModelConverter.get_hashtag_from_dict(hashtag_dict)

        self.assertEqual(hashtag, hashtag_test)

    def test_returns_hashtag_list(self):
        hashtag_dict1 = {'text': '#text1', 'tweet_volume': 1}
        hashtag_dict2 = {'text': '#text2', 'tweet_volume': 1}

        hashtag1 = Hashtag(text='#text1', tweet_volume=1)
        hashtag2 = Hashtag(text='#text2', tweet_volume=1)

        hashtag_test = DictModelConverter.get_hashtag_list([hashtag_dict1, hashtag_dict2])

        self.assertEqual([hashtag1, hashtag2], hashtag_test)
