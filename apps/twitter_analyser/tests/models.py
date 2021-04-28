import datetime

from django.test import TestCase

from apps.twitter_analyser.models import Tweet, TwitterProfile, Hashtag


class ModelsTest(TestCase):
    def test_tweet_was_saved_without_author(self):
        tweet = Tweet.objects.create(tweet_id=123, creation_date=datetime.datetime.now().date(),
                                     save_date=datetime.datetime.now().date(), text='text', retweets=1, likes=1)

    def test_models_relations(self):
        date = datetime.datetime.now().date()
        author = TwitterProfile.objects.create(profile_id=1, username='username', save_date=date)
        tweet = Tweet.objects.create(tweet_id=123, creation_date=date, save_date=date,
                                     text='text', retweets=1, likes=1, author=author)
        hashtag = Hashtag.objects.create(save_date=date, text='#text', tweet_volume=1)
        hashtag.tweets.add(tweet)

        self.assertEqual(tweet.author, author)
        self.assertEqual(hashtag.tweets.first(), tweet)

    def test_models_strs(self):
        date = datetime.datetime.now().date()
        author = TwitterProfile.objects.create(profile_id=1, username='username', save_date=date)
        tweet = Tweet.objects.create(tweet_id=123, creation_date=date, save_date=date,
                                     text='text', retweets=1, likes=1, author=author)
        hashtag = Hashtag.objects.create(save_date=date, text='#text', tweet_volume=1)

        self.assertEqual(str(author), "Twitter profile username with id 1")
        self.assertEqual(str(tweet), f"Tweet posted on {date} with text: text. Posted by username")
        self.assertEqual(str(hashtag), f"#text used by 1 tweets")

    def test_models_eqs(self):
        author1 = TwitterProfile.objects.create(profile_id=1, username='username', save_date=datetime.datetime.now())
        author2 = TwitterProfile.objects.create(profile_id=1, username='username', save_date=datetime.datetime.now())
        tweet1 = Tweet.objects.create(tweet_id=123, creation_date=datetime.datetime.now().date(),
                                     save_date=datetime.datetime.now().date(), text='text', retweets=1, likes=1,
                                     author=author1)
        tweet2 = Tweet.objects.create(tweet_id=123, creation_date=datetime.datetime.now().date(),
                                      save_date=datetime.datetime.now().date(), text='text', retweets=10, likes=10,
                                      author=author2)
        hashtag1 = Hashtag.objects.create(save_date=datetime.datetime.now(), text='#text', tweet_volume=1)
        hashtag2 = Hashtag.objects.create(save_date=datetime.datetime.now(), text='#text', tweet_volume=10)

        self.assertEqual(author1, author2)
        self.assertEqual(tweet1, tweet2)
        self.assertEqual(hashtag1, hashtag2)