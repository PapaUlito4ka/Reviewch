from django.urls import path, include
from django.contrib.auth.views import LoginView

import core.views as views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login', LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True), name='login'),
    path('accounts/register', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('review/<int:id>/', views.review, name='review'),
    path('create_review/', views.create_review, name='create_review'),
]