import datetime

from apps.twitter_analyser.models import Hashtag
from apps.twitter_analyser.utils.plot_painter import PlotPainter


def get_user_specifics_for_date(day, month, year, request):
    appuser = request.user.appuser
    users_hashtags = appuser.hashtag_set.all()
    users_profiles = appuser.twitterprofile_set.all()
    trending_hashtags_from_db = Hashtag.objects.all()
    dates = list(set([hashtag.save_date for hashtag in trending_hashtags_from_db]))
    current_date = datetime.datetime(year, month, day)
    trending_hashtags = Hashtag.objects.filter(appuser__isnull=True).filter(save_date=current_date).distinct()
    return current_date, dates, trending_hashtags, users_hashtags, users_profiles


def handle_trending_hashtags_for_date(trending_hashtags):
    if trending_hashtags:
        trending_hashtags_list = [trending_hashtag for trending_hashtag in trending_hashtags]

        trending_hashtags_list.sort(key=lambda hashtag: hashtag.tweet_volume, reverse=True)
        trending_hashtags_chart = PlotPainter.plot_hashtags(trending_hashtags_list)
    else:
        trending_hashtags_list = None
        trending_hashtags_chart = None
    return trending_hashtags_chart, trending_hashtags_list


def handle_hashtags_tweets_for_date(current_date, current_hashtag):
    hashtags_tweets = current_hashtag.tweets.filter(save_date=current_date).distinct()
    hashtags_tweets_list = [hashtags_tweet for hashtags_tweet in hashtags_tweets]
    hashtags_tweets_list.sort(key=lambda tweet: (tweet.retweets, tweet.likes), reverse=True)
    hashtags_tweets_list = hashtags_tweets_list[:10]
    hashtags_tweets_chart = PlotPainter.plot_tweets(hashtags_tweets_list)
    return hashtags_tweets_chart, hashtags_tweets_list


def handle_profiles_tweets_for_date(current_date, current_profile):
    profiles_tweets = current_profile.tweet_set.filter(save_date=current_date).distinct()
    profiles_tweets_list = [profiles_tweet for profiles_tweet in profiles_tweets]
    profiles_tweets_list.sort(key=lambda tweet: (tweet.retweets, tweet.likes), reverse=True)
    profiles_tweets_list = profiles_tweets_list[:10]
    profiles_tweets_chart = PlotPainter.plot_tweets(profiles_tweets_list)
    return profiles_tweets_chart, profiles_tweets_list
