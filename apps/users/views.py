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
    form_class = UserForm

    def post(self, request):
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
            print(user_form.errors)

        return render(request, 'users/register.html', {'user_form': user_form, 'registered': registered})

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'twitter_analyser/index.html')

        user_form = self.form_class()

        return render(request, 'users/register.html', {'user_form': user_form, 'registered': False})


class LoginView(View):
    form_class = LoginForm

    def post(self, request):
        login_form = self.form_class(request.POST)
        if login_form.is_valid():
            user = authenticate(username=login_form.data['username'], password=login_form.data['password'])
            if user and user.is_active:
                login(request, user)
                return render(request, 'twitter_analyser/index.html')
            else:
                messages.error(request, 'Username or password not correct')
        else:
            print(login_form.errors)

        return render(request, 'users/login.html', {'login_form': login_form})

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'twitter_analyser/index.html')

        login_form = self.form_class()

        return render(request, 'users/login.html', {'login_form': login_form})


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return redirect('users:login')


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users:login')
    template_name = 'users/user_confirm_delete.html'
