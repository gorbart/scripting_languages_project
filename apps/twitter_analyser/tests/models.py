import datetime

from django.test import TestCase

from apps.twitter_analyser.models import Tweet, TwitterProfile, Hashtag


class ModelsTest(TestCase):
    def test_tweet_was_saved_without_author(self):
        tweet = Tweet.objects.create(tweet_id='123', creation_date=datetime.datetime.now().date(),
                                     save_date=datetime.datetime.now().date(), text='text', retweets=1, likes=1,
                                     responses=1)

    def test_models_relations(self):
        date = datetime.datetime.now().date()
        author = TwitterProfile.objects.create(profile_id='1', username='username', save_date=date)
        tweet = Tweet.objects.create(tweet_id='123', creation_date=date, save_date=datetime.datetime.now().date(),
                                     text='text', retweets=1, likes=1, responses=1, author=author)
        hashtag = Hashtag.objects.create(save_date=date, text='#text', tweet_volume=1)
        hashtag.tweets.add(tweet)

        self.assertEqual(tweet.author, author)
        self.assertEqual(hashtag.tweets.first(), tweet)

    def test_models_strs(self):
        date = datetime.datetime.now().date()
        author = TwitterProfile.objects.create(profile_id='1', username='username', save_date=date)
        tweet = Tweet.objects.create(tweet_id='123', creation_date=date, save_date=datetime.datetime.now().date(),
                                     text='text', retweets=1, likes=1, responses=1, author=author)
        hashtag = Hashtag.objects.create(save_date=date, text='#text', tweet_volume=1)

        self.assertEqual(str(author), "Twitter profile username with id 1")
        self.assertEqual(str(tweet), f"Tweet posted on {date} with text: text. Posted by username")
        self.assertEqual(str(hashtag), f"#text used by 1 tweets")
