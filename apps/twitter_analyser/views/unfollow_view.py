from django.shortcuts import redirect


def unfollow_hashtag(request, pk):
    """
    unfollow_hashtag deletes Hashtag object indicated by the user
    :param request: POST request
    :param pk: primary key of deleted Hashtag
    :return: redirection to index page
    """

    if request.method == 'POST':
        request.user.appuser.hashtag_set.get(pk=pk).delete()
    return redirect('twitter_analyser:index')


def unfollow_profile(request, pk):
    """
    unfollow_profile deletes TwitterProfile object indicated by the user
    :param request: POST request
    :param pk: primary key of deleted TwitterProfile
    :return: redirection to index page
    """

    if request.method == 'POST':
        request.user.appuser.twitterprofile_set.get(pk=pk).delete()
    return redirect('twitter_analyser:index')
