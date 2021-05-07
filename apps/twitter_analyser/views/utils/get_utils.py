import datetime

from apps.twitter_analyser.models import Hashtag
from apps.twitter_analyser.utils.plot_painter import PlotPainter


def get_user_specifics(request):
    """
    get_user_specifics retrieves from request and database all data, necessary for later page content rendering, which
    is: AppUser instance, related to logged in user, hashtags and profiles followed by him, trending hashtags, retrieved
    from Twitter API on earlier usages and list of dates of earlier usages.
    :param request: GET request
    :return: lists of dates, earlier trending hashtags, user's followed hashtags and profiles
    """

    appuser = request.user.appuser
    users_hashtags = appuser.hashtag_set.all()
    users_profiles = appuser.twitterprofile_set.all()
    trending_hashtags_from_db = Hashtag.objects.all()
    dates = list(set([hashtag.save_date for hashtag in trending_hashtags_from_db]))
    return dates, trending_hashtags_from_db, users_hashtags, users_profiles


def handle_trending_hashtags(api_pipeline, trending_hashtags_from_db):
    """
    handle_trending_hashtags gets currently trending hashtags from Twitter API, then produces chart showing their
    popularity and saves them in database if they haven't been saved already today.
    :param api_pipeline: TwitterApiPipeline instantiated with project's credentials
    :param trending_hashtags_from_db: list of trending hashtags from earlier app usages
    :return: list of current trending hashtags (retrieved from API) and chart, presenting their popularity
    """

    trending_hashtags = api_pipeline.get_top_hashtags_worldwide()
    trending_hashtags.sort(key=lambda hashtag: hashtag.tweet_volume, reverse=True)
    trending_hashtags_chart = PlotPainter.plot_hashtags(trending_hashtags)
    trending_hashtags_from_db_today = trending_hashtags_from_db.filter(save_date=datetime.datetime.today().date())
    for trending_hashtag in trending_hashtags:
        if trending_hashtag not in trending_hashtags_from_db_today:
            trending_hashtag.save()
    return trending_hashtags, trending_hashtags_chart


def handle_current_hashtag(api_pipeline, current_hashtag):
    """
    handle_current_hashtag gets a hashtag, then retrieves its most popular posts now from Twitter API, then
    produces chart showing the posts' popularity and saves them in database.
    :param api_pipeline: TwitterApiPipeline instantiated with project's credentials
    :param current_hashtag: hashtag, for which the function does all the processing
    :return: list of current hashtags' tweets (retrieved from API) and chart, presenting their popularity
    """

    current_hashtag_saved_tweets = current_hashtag.tweets.all()
    hashtags_tweets = api_pipeline.get_recent_tweets_for_hashtag(current_hashtag.text, how_many=5)
    for hashtags_tweet in hashtags_tweets:
        if hashtags_tweet not in current_hashtag_saved_tweets.filter(save_date=datetime.datetime.today().date()):
            hashtags_tweet.save()
            current_hashtag.tweets.add(hashtags_tweet)
    current_hashtag.save()
    hashtags_tweets.sort(key=lambda tweet: (tweet.retweets, tweet.likes), reverse=True)
    hashtags_tweets_chart = PlotPainter.plot_tweets(hashtags_tweets) if hashtags_tweets else None
    return hashtags_tweets, hashtags_tweets_chart


def handle_current_profile(api_pipeline, current_profile):
    """
    handle_current_profile gets a Twitter profile, then retrieves its most popular posts now from Twitter API, then
    produces chart showing the posts' popularity and saves them in database.
    :param api_pipeline: TwitterApiPipeline instantiated with project's credentials
    :param current_profile: profile, for which the function does all the processing
    :return: list of current profiles' tweets (retrieved from API) and chart, presenting their popularity
    """

    current_profile_saved_tweets = current_profile.tweet_set.all()
    profiles_tweets = api_pipeline.get_recent_tweets_for_author(current_profile.username, how_many=5)
    for profiles_tweet in profiles_tweets:
        if profiles_tweet not in current_profile_saved_tweets.filter(save_date=datetime.datetime.today().date()):
            profiles_tweet.save()
            current_profile.tweet_set.add(profiles_tweet)
    current_profile.save()
    profiles_tweets.sort(key=lambda tweet: (tweet.retweets, tweet.likes), reverse=True)
    profiles_tweets_chart = PlotPainter.plot_tweets(profiles_tweets) if profiles_tweets else None
    return profiles_tweets, profiles_tweets_chart
