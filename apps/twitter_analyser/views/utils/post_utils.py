import datetime

from apps.twitter_analyser.models import Hashtag


def handle_new_following(request, api_pipeline):
    """
    handle_new_following takes POST request and TwitterAPIPipeline instance and with query from the first one uses
    the pipeline to retrieve Hashtag or TwitterProfile with characteristics given by the user and most popular Tweets
    with these new followings. These contents are then stored in the request parameter (it's modified).
    :param request: POST request with search query
    :param api_pipeline: TwitterAPIPipeline instance, used for searching for Tweets, Hashtags and Profiles
    :return user's input - formerly used to create Hashtag or TwitterProfile
    """
    appuser = request.user.appuser
    hashtag_input = request.POST.get('hashtag_input')
    if hashtag_input:
        handle_hashtag_following(api_pipeline, hashtag_input, appuser)

        return hashtag_input

    profile_input = request.POST.get('profile_input')
    if profile_input:
        handle_profile_following(api_pipeline, profile_input, appuser)

        return profile_input


def handle_hashtag_following(api_pipeline, hashtag_input, appuser):
    """
    handle_hashtag_following takes hashtag input query and TwitterAPIPipeline instance. With query uses
    the pipeline to retrieve given Hashtag-related Tweets. Then it checks if this hashtag is not already followed by the
    user. If it isn't and Tweet retrieving was successful, the function saves Hashtag instance and its Tweets. It also
    adds Hashtag to user's followed Hashtags. User is stored in the request parameter (it's modified).
    :param hashtag_input: hashtag's text, given by the user
    :param appuser: AppUser instance, for which we perform the following
    :param api_pipeline: TwitterAPIPipeline instance, used for searching for Tweets, Hashtags and Profiles
    :return user's input - formerly used to create Hashtag
    """

    hashtags_tweets = api_pipeline.get_recent_tweets_for_hashtag(hashtag_input)
    hashtags_from_db = appuser.hashtag_set.filter(text=hashtag_input)
    if hashtags_tweets and not hashtags_from_db:
        hashtag = Hashtag.objects.create(text=hashtag_input, save_date=datetime.datetime.now(),
                                         appuser=appuser)
        for tweet in hashtags_tweets:
            tweet.save()
        hashtag.tweets.add(*hashtags_tweets)
        appuser.hashtag_set.add(hashtag)


def handle_profile_following(api_pipeline, profile_input, appuser):
    """
    handle_profile_following takes profile input query and TwitterAPIPipeline instance. With query uses
    the pipeline to retrieve given Profile-related Tweets. Then it checks if this profile is not already followed by the
    user. If it isn't and Profile retrieving was successful, the function saves TwitterProfile instance and its Tweets.
    It also adds TwitterProfile to user's followed TwitterProfiles. User is stored in the request parameter (it's
    modified).
    :param profile_input: profile's username, given by the user
    :param appuser: AppUser instance, for which we perform the following
    :param api_pipeline: TwitterAPIPipeline instance, used for searching for Tweets, Hashtags and Profiles
    :return user's input - formerly used to create TwitterProfile
    """

    profile_tweets = api_pipeline.get_recent_tweets_for_author(profile_input)
    profiles_from_db = appuser.twitterprofile_set.filter(username=profile_input)
    if profile_tweets and not profiles_from_db:
        profile = api_pipeline.get_twitter_profile(profile_input)
        profile.appuser = appuser
        profile.save()
        for tweet in profile_tweets:
            tweet.save()
        profile.tweet_set.add(*profile_tweets)
        appuser.twitterprofile_set.add(profile)
