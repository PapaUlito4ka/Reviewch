from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import rest_framework.status as status
from django.urls import reverse
from django.contrib.auth import authenticate, login
from core.models import Review

import core.forms as forms
import core.api_requests as api


def home(request: HttpRequest):
    context = {
        'user': request.user,
        'ordering': request.GET.get('ordering', 'created_at'),
        'group': request.GET.get('group', ''),
        'page': request.GET.get('page', 1)
    }
    return render(request, 'home.html', context=context)


def search(request: HttpRequest):
    context = {
        'user': request.user,
        'ordering': request.GET.get('ordering', 'created_at'),
        'group': request.GET.get('group', ''),
        'search': request.GET.get('q', ''),
        'page': request.GET.get('page', 1)
    }
    return render(request, 'search.html', context=context)


@csrf_exempt
def register(request: HttpRequest):
    context = {
        'user': request.user,
    }
    if request.method == 'GET':
        if context['user'].is_authenticated:
            return redirect(reverse('profile', kwargs={'id': context['user'].id}))
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
                return redirect(reverse('profile', kwargs={'id': user.id}))
            context['error'] = res.json()
            return render(request, 'register.html', context=context)
        return render(request, 'register.html', context=context)


@login_required(login_url='/accounts/login')
def profile(request: HttpRequest, id: int = None):
    if not id:
        return redirect(reverse('profile', kwargs={'id': request.user.id}))
    context = {
        'user': request.user,
        'user_id': id,
        'ordering': request.GET.get('ordering', 'created_at'),
        'group': request.GET.get('group', ''),
        'search': request.GET.get('q', ''),
        'page': request.GET.get('page', 1)
    }
    return render(request, 'profile.html', context=context)


def review(request: HttpRequest, id: int):
    context = {
        'user': request.user,
        'review_id': id,
        'form': forms.CommentForm()
    }
    if request.method == 'GET':
        context['form'] = forms.CommentForm()
        try:
            context['review_text'] = Review.objects.get(id=id).text
        except Review.DoesNotExist:
            return render(request, 'not_found.html', context=context)
        return render(request, 'review.html', context=context)
    if request.method == 'POST' and request.user.is_authenticated:
        context['form'] = forms.CommentForm(request.POST)
        if context['form'].is_valid():
            res = api.create_comment(request.POST)
            if res.status_code == status.HTTP_201_CREATED:
                return redirect(reverse('review', kwargs={'id': id}))
            context['error'] = res.json()
            return render(request, 'review.html', context=context)
        return render(request, 'review.html', context=context)


@login_required(login_url='/accounts/login')
def create_review(request: HttpRequest):
    context = {
        'user': request.user
    }
    if request.method == 'GET':
        context['form'] = forms.CreateReviewForm()
        context['form'].fields['user'].initial = request.user.username
        return render(request, 'create_review.html', context=context)
    if request.method == 'POST':
        context['form'] = forms.CreateReviewForm(request.POST, request.FILES)
        if context['form'].is_valid():
            res = api.create_review(request.POST)
            if res.status_code == status.HTTP_201_CREATED:
                if len(request.FILES.getlist('images')) != 0:
                    res = api.create_review_images(res.json(), request.FILES)
                    if res.status_code == status.HTTP_201_CREATED:
                        return redirect(reverse('profile', kwargs={'id': context['user'].id}))
                return redirect(reverse('profile', kwargs={'id': context['user'].id}))
            context['error'] = res.json()
            return render(request, 'create_review.html', context=context)
        return render(request, 'create_review.html', context=context)


@login_required(login_url='/account/login')
def edit_review(request: HttpRequest, id: int):
    context = {
        'user': request.user,
        'review_id': id
    }
    if request.method == 'GET':
        res = api.get_review(id)
        if res.status_code == status.HTTP_200_OK:
            data = res.json()
            context['form'] = forms.CreateReviewForm(
                initial={
                    'user': data['author_username'],
                    'title': data['title'],
                    'group': data['group'],
                    'text': data['text'],
                    'rating': data['rating'],
                    'tags': ' '.join(data['tags'])
                }
            )
            return render(request, 'edit_review.html', context=context)
        return render(request, 'not_found.html', context=context)
    if request.method == 'POST':
        context['form'] = forms.CreateReviewForm(request.POST, request.FILES)
        if context['form'].is_valid():
            res = api.update_review(request.POST, id)
            if res.status_code == status.HTTP_200_OK:
                if len(request.FILES.getlist('images')) != 0:
                    res = api.create_review_images(res.json(), request.FILES)
                    if res.status_code == status.HTTP_201_CREATED:
                        return redirect(reverse('profile', kwargs={'id': context['user'].id}))
                return redirect(reverse('profile', kwargs={'id': context['user'].id}))
            context['error'] = res.json()
            return render(request, 'edit_review.html', context=context)
        return render(request, 'edit_review.html', context=context)


def tags(request: HttpRequest):
    context = {
        'user': request.user
    }
    return render(request, 'tags.html', context=context)


@user_passes_test(
    lambda user: user.is_authenticated,
    login_url='/accounts/login',
    redirect_field_name='next'
)
@user_passes_test(
    lambda user: user.is_staff,
    login_url='/profile',
    redirect_field_name='next'
)
def users(request: HttpRequest):
    context = {
        'user': request.user
    }
    return render(request, 'users.html', context=context)



