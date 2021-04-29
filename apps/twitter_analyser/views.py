from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View


class IndexView(View):

    @login_required(login_url='/users/login/')
    def get(self):
        return render(self.request, 'twitter_analyser/index.html')
