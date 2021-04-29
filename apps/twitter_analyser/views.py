from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class IndexView(View, LoginRequiredMixin):
    raise_exception = False
    login_url = 'users/login'

    def get(self, request):
        return render(request, 'twitter_analyser/index.html')
