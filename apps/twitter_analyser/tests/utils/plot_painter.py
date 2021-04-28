import tempfile
import webbrowser

from datetime import datetime

from django.test import SimpleTestCase

from apps.twitter_analyser.models import Tweet, Hashtag
from apps.twitter_analyser.utils.plot_painter import PlotPainter


class PlotPainterTest(SimpleTestCase):

    def test_tweet_plot(self):
        date = datetime.now().date()
        tweet1 = Tweet(tweet_id=1, creation_date=date, text='text1', save_date=datetime.now(), retweets=30,
                       likes=100)

        tweet2 = Tweet(tweet_id=2, creation_date=date, text='text2', save_date=datetime.now(), retweets=50,
                       likes=20)
        tweets = [tweet1, tweet2]

        plot = PlotPainter.plot_tweets(tweets)

        fh, path = tempfile.mkstemp(suffix='.html')
        url = 'file://' + path

        with open(path, 'w') as fp:
            fp.write(plot)
        webbrowser.open(url)

    def test_hashtag_plot(self):
        hashtag1 = Hashtag(text='#text1', tweet_volume=100)
        hashtag2 = Hashtag(text='#text2', tweet_volume=10)
        hashtags = [hashtag1, hashtag2]

        plot = PlotPainter.plot_hashtags(hashtags)

        fh, path = tempfile.mkstemp(suffix='.html')
        url = 'file://' + path

        with open(path, 'w') as fp:
            fp.write(plot)
        webbrowser.open(url)

