from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import rest_framework.status as status
from django.urls import reverse
from django.contrib.auth import authenticate, login

import core.forms as forms
import core.api_requests as api


def home(request: HttpRequest):
    context = {
        'user': request.user
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
        context['form'] = forms.RegisterForm()
        return render(request, 'register.html', context=context)
    if request.method == 'POST':
        context['form'] = forms.RegisterForm(request.POST)
        if context['form'].is_valid():
            res = api.create_user(request.POST)
            if res.status_code == status.HTTP_201_CREATED:
                user = authenticate(
                    request,
                    username=request.POST.get('username'),
                    password=request.POST.get('password')
                )
                login(request, user)
                return redirect(reverse('profile'))
            context['error'] = res.json()
            return render(request, 'register.html', context=context)
        return render(request, 'register.html', context=context)


@login_required(login_url='/accounts/login')
def profile(request: HttpRequest):
    context = {
        'user': request.user
    }
    return render(request, 'profile.html', context=context)


def review(request: HttpRequest, id: int):
    context = {
        'user': request.user,
        'review_id': id
    }
    return render(request, 'review.html', context=context)


@login_required(login_url='/accounts/login')
def create_review(request: HttpRequest):
    context = {
        'user': request.user
    }
    if request.method == 'GET':
        context['form'] = forms.CreateReviewForm()
        return render(request, 'create_review.html', context=context)
    if request.method == 'POST':
        context['form'] = forms.CreateReviewForm(request.POST, request.FILES)
        if context['form'].is_valid():
            res = api.create_review(request.POST)
            if res.status_code == status.HTTP_201_CREATED:
                res = api.create_review_images(res.json(), request.FILES)
                if res.status_code == status.HTTP_201_CREATED:
                    return redirect(reverse('profile'))
            context['error'] = res.json()
            return render(request, 'create_review.html', context=context)
        return render(request, 'create_review.html', context=context)



