import datetime

from django.contrib.auth.models import User
from django.test import SimpleTestCase, override_settings

from apps.twitter_analyser.models import Tweet, Hashtag, TwitterProfile
from apps.twitter_analyser.utils.email_report_sender import EmailReportSender


@override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
class EmailReportSenderTest(SimpleTestCase):

    def test_send_report(self):
        user = User(username='username', password='password', email='example@example.com')
        current_hashtag1 = Hashtag(text='#text1', tweet_volume=100)
        current_hashtag2 = Hashtag(text='#text2', tweet_volume=100)

        trending_hashtags = [current_hashtag1, current_hashtag2]

        current_date = datetime.datetime.now().date()
        tweet1 = Tweet(tweet_id=1, creation_date=current_date, text='text1', save_date=datetime.datetime.now(),
                       retweets=30, likes=100)

        tweet2 = Tweet(tweet_id=2, creation_date=current_date, text='text2', save_date=datetime.datetime.now(),
                       retweets=50, likes=20)
        tweets = [tweet1, tweet2]

        current_profile = TwitterProfile(profile_id=1, username='username', save_date=current_date)

        context = {'user': user, 'trending_hashtags': trending_hashtags, 'current_date': current_date,
                   'current_hashtag': current_hashtag1, 'hashtags_tweets': tweets, 'current_profile': current_profile,
                   'profiles_tweets': tweets}

        EmailReportSender.send_report(context)
