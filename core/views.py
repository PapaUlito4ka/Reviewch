from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
import django
import rest_framework.status as status
from django.urls import reverse

from core.forms import RegisterForm
from core.models import User
import core.api_requests as api


def home(request: HttpRequest):
    context = {
        'session': request.session
    }
    return render(request, 'home.html', context=context)


@csrf_exempt
def register(request: HttpRequest):
    context = {
        'user': request.user,
    }
    if request.method == 'GET':
        if context['user'].is_authenticated:
            return redirect(reverse('profile'))
        context['form'] = RegisterForm()
        return render(request, 'register.html', context=context)
    if request.method == 'POST':
        context['form'] = RegisterForm(request.POST)
        if context['form'].is_valid():
            res = api.create_user(request.POST)
            if res.status_code == status.HTTP_201_CREATED:
                return redirect(reverse('profile'))
            context['error'] = res.json()
            return render(request, 'register.html', context=context)
        return render(request, 'register.html', context=context)


@login_required(login_url='/accounts/login')
def profile(request: HttpRequest):
    context = {
        'session': request.session
    }
    return render(request, 'profile.html', context=context)


def review(request: HttpRequest):
    context = {
        'session': request.session
    }
    return render(request, 'review.html', context=context)



