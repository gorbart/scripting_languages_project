import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from apps.twitter_analyser.models import TwitterProfile, Tweet, Hashtag
from apps.users.models import AppUser


class AppUserTest(TestCase):

    def test_appuser_relations(self):
        user = User.objects.create(username='username', password='password')
        appuser = AppUser.objects.create(user=user)
        author1 = TwitterProfile.objects.create(profile_id=1, username='username', save_date=datetime.datetime.now(),
                                                appuser=appuser)
        author2 = TwitterProfile.objects.create(profile_id=2, username='username1', save_date=datetime.datetime.now(),
                                                appuser=appuser)
        tweet1 = Tweet.objects.create(tweet_id=123, creation_date=datetime.datetime.now().date(),
                                      save_date=datetime.datetime.now().date(), text='text', retweets=1, likes=1,
                                      author=author1)
        tweet2 = Tweet.objects.create(tweet_id=124, creation_date=datetime.datetime.now().date(),
                                      save_date=datetime.datetime.now().date(), text='text1', retweets=10, likes=10,
                                      author=author2)
        hashtag1 = Hashtag.objects.create(save_date=datetime.datetime.now(), text='#text', tweet_volume=1,
                                          appuser=appuser)
        hashtag1.tweets.add(tweet1, tweet2)
        hashtag2 = Hashtag.objects.create(save_date=datetime.datetime.now(), text='#text1', tweet_volume=10)
        hashtag2.tweets.add(tweet1, tweet2)
        appuser.hashtag_set.add(hashtag1)
        appuser.hashtag_set.add(hashtag2)
        appuser.twitterprofile_set.add(author1)
        appuser.twitterprofile_set.add(author2)

        self.assertEqual(appuser.hashtag_set.count(), 2)
        self.assertEqual(appuser.twitterprofile_set.count(), 2)
        self.assertEqual(appuser.hashtag_set.first().tweets.count(), 2)

    def test_appuser_deletions(self):
        user = User.objects.create(username='username', password='password')
        appuser = AppUser.objects.create(user=user)
        author1 = TwitterProfile.objects.create(profile_id=1, username='username', save_date=datetime.datetime.now(),
                                                appuser=appuser)
        author2 = TwitterProfile.objects.create(profile_id=2, username='username1', save_date=datetime.datetime.now(),
                                                appuser=appuser)
        tweet1 = Tweet.objects.create(tweet_id=123, creation_date=datetime.datetime.now().date(),
                                      save_date=datetime.datetime.now().date(), text='text', retweets=1, likes=1,
                                      author=author1)
        tweet2 = Tweet.objects.create(tweet_id=124, creation_date=datetime.datetime.now().date(),
                                      save_date=datetime.datetime.now().date(), text='text1', retweets=10, likes=10,
                                      author=author2)
        hashtag1 = Hashtag.objects.create(save_date=datetime.datetime.now(), text='#text', tweet_volume=1,
                                          appuser=appuser)
        hashtag1.tweets.add(tweet1, tweet2)
        hashtag2 = Hashtag.objects.create(save_date=datetime.datetime.now(), text='#text1', tweet_volume=10)
        hashtag2.tweets.add(tweet1, tweet2)
        appuser.hashtag_set.add(hashtag1)
        appuser.hashtag_set.add(hashtag2)
        appuser.twitterprofile_set.add(author1)
        appuser.twitterprofile_set.add(author2)

        appuser.delete()
        user.delete()

        self.assertEqual(Hashtag.objects.count(), 2)
        self.assertEqual(TwitterProfile.objects.count(), 0)
