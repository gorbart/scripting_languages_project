from django.test import SimpleTestCase

import credentials
from apps.twitter_analyser.utils.twitter_api_handler import TwitterApiHandler


class TwitterApiHandlerTest(SimpleTestCase):

    def test_returns_hashtags_with_volume(self):
        api_handler = TwitterApiHandler(credentials.TWITTER_KEY, credentials.TWITTER_SECRET)
        hashtags = api_handler.get_trending_hashtags()
        self.assertTrue(hashtags[0]['text'][0] == '#')
        self.assertTrue(hashtags[0]['volume'] > 0)

    def test_returns_tweets(self):
        tweets_num = 25
        hashtag = '#Django'
        api_handler = TwitterApiHandler(credentials.TWITTER_KEY, credentials.TWITTER_SECRET)
        tweets = api_handler.get_tweets_with_hashtag(hashtag, tweets_num)
        self.assertEqual(len(tweets), tweets_num)
        self.assertTrue(hashtag.lower() in tweets[0]['text'].lower())

    def test_returns_user_by_name(self):
        username = 'djangoproject'
        api_handler = TwitterApiHandler(credentials.TWITTER_KEY, credentials.TWITTER_SECRET)
        user = api_handler.get_user(username)
        self.assertEqual(user['username'], username)

    def test_returns_user_by_id(self):
        profile_id = 191225303
        api_handler = TwitterApiHandler(credentials.TWITTER_KEY, credentials.TWITTER_SECRET)
        user = api_handler.get_user(profile_id)
        self.assertEqual(user['profile_id'], profile_id)
