from django.http import HttpResponseNotFound
from django.shortcuts import redirect


def view_404(request, exception=None):
    return HttpResponseNotFound('/')


def main_view(request):
    return redirect('twitter_analyser:index')

