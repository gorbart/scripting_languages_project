def get_all_dates_for_user(users_hashtags, users_profiles, trending_hashtags_from_db):
    hashtag_dates = [hashtag.save_date for hashtag in users_hashtags]
    profile_dates = [profile.save_date for profile in users_profiles]
    trending_hashtags_from_db_dates = [hashtag.save_date for hashtag in trending_hashtags_from_db]
    hashtag_tweet_dates = [tweet.save_date for hashtag in users_hashtags for tweet in hashtag.tweets.all()]
    profile_tweet_dates = [tweet.save_date for profile in users_profiles for tweet in profile.tweets.all()]
    dates = set(hashtag_dates + profile_dates + hashtag_tweet_dates + profile_tweet_dates
                + trending_hashtags_from_db_dates)
    return list(dates)
