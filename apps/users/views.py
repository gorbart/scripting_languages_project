import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from apps.users.forms import UserForm, LoginForm
from apps.users.models import AppUser


class RegisterView(View):
    """
    Class RegisterView is used to render register html page and add new app's users
    """

    logger = logging.getLogger(__name__)
    form_class = UserForm

    def post(self, request):
        """
        POST method gets registration form and checks for its validity. If it's valid, it creates Django User class
        instance, sets its password, creates companion object AppUser and saves them in database
        :param request: POST request
        :return: register.html page with appropriate message and form
        """

        user_form = self.form_class(request.POST)
        registered = False
        if user_form.is_valid():

            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            appuser = AppUser()
            appuser.user = user
            appuser.save()
            registered = True
        else:
            self.logger.error(user_form.errors)

        return render(request, 'users/register.html', {'user_form': user_form, 'registered': registered})

    def get(self, request):
        """
        GET method renders registration page if user is not logged in and index page if he is
        :param request: GET request
        :return: register.html page with appropriate message and form or index page
        """

        if request.user.is_authenticated:
            return render(request, 'twitter_analyser/index.html')

        user_form = self.form_class()

        return render(request, 'users/register.html', {'user_form': user_form, 'registered': False})


class LoginView(View):
    """
    Class LoginView is used to render login html page and allow app's users to log in it
    """

    logger = logging.getLogger(__name__)
    form_class = LoginForm

    def post(self, request):
        """
        POST method gets login form and checks for its validity. If it's valid, it tries to authenticate Django User
        class instance
        :param request: POST request
        :return: index page if user successfully logged in or login page with appropriate message and form otherwise
        """

        login_form = self.form_class(request.POST)
        if login_form.is_valid():
            user = authenticate(username=login_form.data['username'], password=login_form.data['password'])
            if user and user.is_active:
                login(request, user)
                return render(request, 'twitter_analyser/index.html')
            else:
                messages.error(request, 'Username or password not correct')
        else:
            self.logger.error(login_form.errors)

        return render(request, 'users/login.html', {'login_form': login_form})

    def get(self, request):
        """
        GET method renders login page if user is not logged in and index page if he is
        :param request: GET request
        :return: login page with appropriate message and form or index page
        """

        if request.user.is_authenticated:
            return render(request, 'twitter_analyser/index.html')

        login_form = self.form_class()

        return render(request, 'users/login.html', {'login_form': login_form})


class LogoutView(LoginRequiredMixin, View):
    """
    Class LogoutView is used to log user out; earlier authentication is of course required
    """

    def get(self, request):
        """
        method logs user out in the app (if he is earlier logged in) and redirects him to login page
        :param request: GET request
        :return: redirect to login page
        """

        logout(request)
        return redirect('users:login')


class DeleteUserView(LoginRequiredMixin, DeleteView):
    """
    DeleteUserView class extends Django template class DeleteView to use it for deleting users from database. User must
    be earlier logged in. After deletion app user is redirected to login page. There is also a intermediate html page
    asking for confirmation of deletion.
    """

    model = User
    success_url = reverse_lazy('users:login')
    template_name = 'users/user_confirm_delete.html'
