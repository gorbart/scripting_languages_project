from django.test import SimpleTestCase

import credentials
from apps.twitter_analyser.utils.twitter_api_pipeline import TwitterApiPipeline


class TwitterApiPipelineTest(SimpleTestCase):

    api_pipeline = TwitterApiPipeline(credentials.TWITTER_KEY, credentials.TWITTER_SECRET)

    def test_returns_hashtags_with_volume(self):
        hashtags_num = 10
        hashtags = self.api_pipeline.get_top_hashtags_worldwide(hashtags_num)
        self.assertTrue(hashtags[0].text[0] == '#')
        self.assertTrue(hashtags[0].tweet_volume > 0)

    def test_returns_tweets_with_hashtag(self):
        tweets_num = 25
        hashtag = '#Django'
        tweets = self.api_pipeline.get_recent_tweets_for_hashtag(hashtag, tweets_num)
        self.assertEqual(len(tweets), tweets_num)
        self.assertTrue(hashtag.lower() in tweets[0].text.lower())

    def test_returns_tweets_with_author(self):
        tweets_num = 25
        author = 'djangoproject'
        tweets = self.api_pipeline.get_recent_tweets_for_author(author, tweets_num)
        self.assertEqual(len(tweets), tweets_num)

    def test_returns_user_by_name(self):
        username = 'djangoproject'
        user = self.api_pipeline.get_twitter_profile(username)
        self.assertEqual(user.username, username)

    def test_returns_user_by_id(self):
        profile_id = 191225303
        user = self.api_pipeline.get_twitter_profile(profile_id)
        self.assertEqual(user.profile_id, profile_id)
