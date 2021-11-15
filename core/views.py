from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


def home(request: HttpRequest):
    context = {
        'session': request.session
    }
    return render(request, 'home.html', context=context)


@csrf_exempt
def login(request: HttpRequest):
    context = {
        'session': request.session
    }

    if request.method == 'GET':
        return render(request, 'login.html', context=context)
    if request.method == 'POST':
        return render(request, 'login.html', context=context)


@csrf_exempt
def register(request: HttpRequest):
    context = {
        'session': request.session
    }
    if request.method == 'GET':
        return render(request, 'register.html', context=context)
    if request.method == 'POST':
        return render(request, 'register.html', context=context)


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


def logout(request: HttpRequest):
    context = {
        'session': request.session
    }
    if request.session:
        request.session.clear()
        return redirect('home', context=context)
    context['error'] = 'Cannot logout being anonymous user'
    redirect('home', context=context)



