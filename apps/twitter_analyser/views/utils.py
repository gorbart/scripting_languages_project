import datetime

from apps.twitter_analyser.models import Hashtag


def get_all_dates_for_user(users_hashtags, users_profiles, trending_hashtags_from_db):
    hashtag_dates = [hashtag.save_date for hashtag in users_hashtags]
    profile_dates = [profile.save_date for profile in users_profiles]
    trending_hashtags_from_db_dates = [hashtag.save_date for hashtag in trending_hashtags_from_db]
    hashtag_tweet_dates = [tweet.save_date for hashtag in users_hashtags for tweet in hashtag.tweets.all()]
    profile_tweet_dates = [tweet.save_date for profile in users_profiles for tweet in profile.tweet_set.all()]
    dates = set(hashtag_dates + profile_dates + hashtag_tweet_dates + profile_tweet_dates
                + trending_hashtags_from_db_dates)
    return list(dates)


def handle_new_following(request, api_pipeline):
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
