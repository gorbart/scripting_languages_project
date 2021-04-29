from django.shortcuts import render
from django.views import View

from apps.users.forms import UserForm
from apps.users.models import AppUser


class RegisterView(View):
    form_class = UserForm

    def post(self, request):
        user_form = self.form_class(request.POST)
        registered = False
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            appuser = AppUser()
            appuser.user = user
            appuser.save()
            registered = True
        else:
            print(user_form.errors)

        return render(request, 'users/register.html', {'user_form': user_form, 'registered': registered})

    def get(self, request):
        user_form = self.form_class()

        return render(request, 'users/register.html', {'user_form': user_form, 'registered': False})
