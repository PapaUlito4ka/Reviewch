from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import rest_framework.status as status
from django.urls import reverse
from django.contrib.auth import authenticate, login
from rest_framework.exceptions import ValidationError

from core.models import Review, User

import core.forms as forms
import core.api_requests as api
import core.services as services
from core.exceptions import handle_error


def home(request: HttpRequest):
    context = {
        'ordering': request.GET.get('ordering', 'created_at'),
        'group': request.GET.get('group', ''),
        'page': request.GET.get('page', 1),
        'language': request.COOKIES.get('language', 'english')
    }
    return render(request, 'home.html', context=context)


def search(request: HttpRequest):
    context = {
        'ordering': request.GET.get('ordering', 'created_at'),
        'group': request.GET.get('group', ''),
        'search': request.GET.get('q', ''),
        'page': request.GET.get('page', 1),
        'language': request.session.get('language', 'english')
    }
    return render(request, 'search.html', context=context)


@csrf_exempt
def register(request: HttpRequest):
    context = {
        'language': request.COOKIES.get('language', 'english')
    }
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(reverse('profile', kwargs={'id': request.user.id}))
        context['form'] = forms.RegisterForm()
        return render(request, 'register.html', context=context)

    if request.method == 'POST':
        context['form'] = forms.RegisterForm(request.POST)
        if context['form'].is_valid():
            try:
                created_user = services.UserService.create(request.POST)
            except ValidationError as e:
                handle_error(context, e)
                return render(request, 'register.html', context=context)
            user = authenticate(
                request,
                username=created_user.username,
                password=created_user.password
            )
            login(request, user)
            return redirect(reverse('profile', kwargs={'id': user.id}))
        return render(request, 'register.html', context=context)


@login_required(login_url='/accounts/login')
def profile(request: HttpRequest, id: int = None):
    if not id:
        return redirect(reverse('profile', kwargs={'id': request.user.id}))
    context = {
        'user_id': id,
        'ordering': request.GET.get('ordering', 'created_at'),
        'group': request.GET.get('group', ''),
        'search': request.GET.get('q', ''),
        'page': request.GET.get('page', 1),
        'language': request.COOKIES.get('language', 'english')
    }
    return render(request, 'profile.html', context=context)


def review(request: HttpRequest, id: int):
    context = {
        'review_id': id,
        'form': forms.CommentForm(),
        'language': request.COOKIES.get('language', 'english')
    }
    if request.method == 'GET':
        context['form'] = forms.CommentForm()
        try:
            services.ReviewService.get(id)
        except Review.DoesNotExist:
            return render(request, 'not_found.html', context=context)
        return render(request, 'review.html', context=context)

    if request.method == 'POST' and request.user.is_authenticated:
        context['form'] = forms.CommentForm(request.POST)
        if context['form'].is_valid():
            try:
                services.CommentService.create(request.POST)
            except ValidationError as e:
                handle_error(context, e)
        return render(request, 'review.html', context=context)


@login_required(login_url='/accounts/login')
def create_review(request: HttpRequest):
    context = {
        'language': request.COOKIES.get('language', 'english')
    }
    if request.method == 'GET':
        context['form'] = forms.CreateReviewForm()
        context['form'].fields['user'].choices = [(user.username, user.username) for user in User.objects.all()]
        context['form'].fields['user'].initial = request.user.username
        return render(request, 'create_review.html', context=context)

    if request.method == 'POST':
        context['form'] = forms.CreateReviewForm(request.POST, request.FILES)
        if context['form'].is_valid():
            try:
                created_review = services.ReviewService.create(request.POST)
                services.ImageService.create(created_review.id, request.FILES)
            except ValidationError as e:
                handle_error(context, e)
                return render(request, 'create_review.html', context=context)
            return redirect(reverse('profile', kwargs={'id': request.user.id}))
        return render(request, 'create_review.html', context=context)


@login_required(login_url='/account/login')
def edit_review(request: HttpRequest, id: int):
    if not request.user.reviews.filter(id=id).exists() and not request.user.is_staff:
        return redirect('/profile')
    context = {
        'review_id': id,
        'language': request.COOKIES.get('language', 'english')
    }
    if request.method == 'GET':
        try:
            review_ = services.ReviewService.get(id)
        except Review.DoesNotExist:
            return render(request, 'not_found.html', context=context)
        context['form'] = forms.CreateReviewForm()
        context['form'].fields['user'].choices = [(user.username, user.username) for user in User.objects.all()]
        context['form'].initial = {
            'user': review_['author_username'],
            'title': review_['title'],
            'group': review_['group'],
            'text': review_['text'],
            'rating': review_['rating'],
            'tags': ' '.join(review_['tags'])
        }
        return render(request, 'edit_review.html', context=context)
    if request.method == 'POST':
        context['form'] = forms.CreateReviewForm(request.POST, request.FILES)
        if context['form'].is_valid():
            try:
                services.ReviewService.update(id, request.POST, request.FILES)
            except ValidationError as e:
                handle_error(context, e)
                return render(request, 'edit_review.html', context=context)
            return redirect(reverse('profile', kwargs={'id': request.user.id}))
        return render(request, 'edit_review.html', context=context)


def tags(request: HttpRequest):
    context = {
        'language': request.COOKIES.get('language', 'english')
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
        'language': request.COOKIES.get('language', 'english')
    }
    return render(request, 'users.html', context=context)


def set_english_language(request: HttpRequest):
    res = redirect(request.GET.get('next', '/'))
    res.set_cookie('language', 'english')
    return res


def set_russian_language(request: HttpRequest):
    res = redirect(request.GET.get('next', '/'))
    res.set_cookie('language', 'russian')
    return res




