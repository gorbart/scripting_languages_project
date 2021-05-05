import datetime

from apps.twitter_analyser.models import Hashtag


def handle_new_following(request, api_pipeline):
    """
    handle_new_following takes POST request and TwitterAPIPipeline instances and with query from the first one uses
    the pipeline to retrieve Hashtag or TwitterProfile with characteristics given by the user and most Tweets with these
    new followings. These contents are then stored in the request parameter (it's modified).
    :param request: POST request with search query
    :param api_pipeline: TwitterAPIPipeline instance, used for searching for Tweets, Hashtags and Profiles
    """

    hashtag_input = request.POST.get('hashtag_input')
    if hashtag_input:
        hashtags_tweets = api_pipeline.get_recent_tweets_for_hashtag(hashtag_input)
        hashtags_from_db = request.user.appuser.followed_hashtags.filter(text=hashtag_input)
        if hashtags_tweets and not hashtags_from_db:
            hashtag = Hashtag.objects.create(text=hashtag_input, save_date=datetime.datetime.now())
            for tweet in hashtags_tweets:
                tweet.save()
            hashtag.tweets.add(*hashtags_tweets)
            request.user.appuser.followed_hashtags.add(hashtag)

    profile_input = request.POST.get('profile_input')
    if profile_input:
        profile_tweets = api_pipeline.get_recent_tweets_for_author(profile_input)
        profiles_from_db = request.user.appuser.followed_profiles.filter(username=profile_input)
        if profile_tweets and not profiles_from_db:
            profile = api_pipeline.get_twitter_profile(profile_input)
            profile.save()
            for tweet in profile_tweets:
                tweet.save()
            profile.tweet_set.add(*profile_tweets)
            request.user.appuser.followed_profiles.add(profile)
