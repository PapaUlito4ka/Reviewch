from django.urls import path, include, re_path
from django.contrib.auth.views import LoginView

import core.views as views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login', LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True), name='login'),
    path('accounts/register', views.register, name='register'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('profile/', views.profile),
    path('review/<int:id>/', views.review, name='review'),
    path('create_review/', views.create_review, name='create_review'),
    path('edit_review/<int:id>/', views.edit_review, name='edit_review'),
    path('tags/', views.tags, name='tags'),
    path('users/', views.users, name='users'),
    path('social_auth/', include('social_django.urls'), name='social_auth'),
]