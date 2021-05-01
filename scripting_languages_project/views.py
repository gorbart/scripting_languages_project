from django.http import HttpResponseNotFound
from django.shortcuts import redirect


def view_404(request, exception=None):
    return HttpResponseNotFound('/')
