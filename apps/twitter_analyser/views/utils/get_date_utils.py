import datetime

from apps.twitter_analyser.models import Hashtag
from apps.twitter_analyser.utils.plot_painter import PlotPainter


def get_user_specifics_for_date(day, month, year, request):
    """
    get_user_specifics_for_date retrieves from request and database all data, necessary for later page content
    rendering, which are: AppUser instance, related to logged in user, hashtags and profiles followed by him, current
    (in the terms of the app) date (given by the user), trending hashtags retrieved from database saved on current date,
    on app's earlier usages and list of dates of earlier usages.
    :param day: current date's day
    :param month: current date's month
    :param year: current date's year
    :param request: GET request
    :return: current date, lists of dates, earlier trending hashtags, user's followed hashtags and profiles
    """

    appuser = request.user.appuser
    users_hashtags = appuser.hashtag_set.all()
    users_profiles = appuser.twitterprofile_set.all()
    trending_hashtags_from_db = Hashtag.objects.all()
    dates = list(set([hashtag.save_date for hashtag in trending_hashtags_from_db]))
    current_date = datetime.datetime(year, month, day)
    trending_hashtags = Hashtag.objects.filter(appuser__isnull=True).filter(save_date=current_date).distinct()
    return current_date, dates, trending_hashtags, users_hashtags, users_profiles


def handle_trending_hashtags_for_date(trending_hashtags):
    """
    handle_trending_hashtags_for_date gets trending hashtags' set from database, converts it to a list, then produces
    a chart showing their popularity.
    :param trending_hashtags: set of trending hashtags from earlier app usages
    :return: chart showing popularity of earlier trending hashtags and a list of current trending hashtags (retrieved
    from API)
    """

    if trending_hashtags:
        trending_hashtags_list = [trending_hashtag for trending_hashtag in trending_hashtags]

        trending_hashtags_list.sort(key=lambda hashtag: hashtag.tweet_volume, reverse=True)
        trending_hashtags_chart = PlotPainter.plot_hashtags(trending_hashtags_list)
    else:
        trending_hashtags_list = None
        trending_hashtags_chart = None
    return trending_hashtags_chart, trending_hashtags_list


def handle_hashtags_tweets_for_date(current_date, current_hashtag):
    """
    handle_hashtags_tweets_for_date gets a hashtag and a date, then gets list of Tweets' saved on given date from
    database and produces a chart of their popularity
    :param current_date: date, which should be save date of hashtag
    :param current_hashtag: hashtag, for which the function does all the processing
    :return: chart presenting current hashtag's tweets' popularity, list of current hashtag's tweets (retrieved from
    database)
    """

    hashtags_tweets = current_hashtag.tweets.filter(save_date=current_date).distinct()
    hashtags_tweets_list = [hashtags_tweet for hashtags_tweet in hashtags_tweets]
    hashtags_tweets_list.sort(key=lambda tweet: (tweet.retweets, tweet.likes), reverse=True)
    hashtags_tweets_list = hashtags_tweets_list[:10]
    hashtags_tweets_chart = PlotPainter.plot_tweets(hashtags_tweets_list) if hashtags_tweets else None
    return hashtags_tweets_chart, hashtags_tweets_list


def handle_profiles_tweets_for_date(current_date, current_profile):
    """
    handle_profiles_tweets_for_date gets a profile and a date, then gets list of Tweets' saved on given date from
    database and produces a chart of their popularity
    :param current_date: date, which should be save date of profile
    :param current_profile: profile, for which the function does all the processing
    :return: chart, presenting current profile's tweets' popularity, list of current profile's tweets (retrieved from
    database)
    """

    profiles_tweets = current_profile.tweet_set.filter(save_date=current_date).distinct()
    profiles_tweets_list = [hashtags_tweet for hashtags_tweet in profiles_tweets]
    profiles_tweets_list.sort(key=lambda tweet: (tweet.retweets, tweet.likes), reverse=True)
    profiles_tweets_list = profiles_tweets_list[:10]
    profiles_tweets_chart = PlotPainter.plot_tweets(profiles_tweets_list) if profiles_tweets else None
    return profiles_tweets_chart, profiles_tweets_list
