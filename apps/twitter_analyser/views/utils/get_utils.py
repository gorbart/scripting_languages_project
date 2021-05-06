from apps.twitter_analyser.models import Hashtag
from apps.twitter_analyser.utils.plot_painter import PlotPainter


def get_user_specifics(request):
    appuser = request.user.appuser
    users_hashtags = appuser.hashtag_set.all()
    users_profiles = appuser.twitterprofile_set.all()
    trending_hashtags_from_db = Hashtag.objects.all()
    dates = list(set([hashtag.save_date for hashtag in trending_hashtags_from_db]))
    return dates, trending_hashtags_from_db, users_hashtags, users_profiles


def handle_trending_hashtags(api_pipeline, trending_hashtags_from_db):
    trending_hashtags = api_pipeline.get_top_hashtags_worldwide()
    trending_hashtags.sort(key=lambda hashtag: hashtag.tweet_volume, reverse=True)
    trending_hashtags_chart = PlotPainter.plot_hashtags(trending_hashtags)
    for trending_hashtag in trending_hashtags:
        if trending_hashtag not in trending_hashtags_from_db:
            trending_hashtag.save()
    return trending_hashtags, trending_hashtags_chart


def handle_current_hashtag(api_pipeline, current_hashtag):
    current_hashtag_saved_tweets = current_hashtag.tweets.all()
    hashtags_tweets = api_pipeline.get_recent_tweets_for_hashtag(current_hashtag.text, how_many=5)
    for hashtags_tweet in hashtags_tweets:
        if hashtags_tweet not in current_hashtag_saved_tweets:
            hashtags_tweet.save()
            current_hashtag.tweets.add(hashtags_tweet)
    current_hashtag.save()
    hashtags_tweets.sort(key=lambda tweet: (tweet.retweets, tweet.likes), reverse=True)
    hashtags_tweets_chart = PlotPainter.plot_tweets(hashtags_tweets)
    return hashtags_tweets, hashtags_tweets_chart


def handle_current_profile(api_pipeline, current_profile):
    current_profile_saved_tweets = current_profile.tweet_set.all()
    profiles_tweets = api_pipeline.get_recent_tweets_for_author(current_profile.username, how_many=5)
    for profiles_tweet in profiles_tweets:
        if profiles_tweet not in current_profile_saved_tweets:
            profiles_tweet.save()
            current_profile.tweet_set.add(profiles_tweet)
    current_profile.save()
    profiles_tweets.sort(key=lambda tweet: (tweet.retweets, tweet.likes), reverse=True)
    profiles_tweets_chart = PlotPainter.plot_tweets(profiles_tweets)
    return profiles_tweets, profiles_tweets_chart
