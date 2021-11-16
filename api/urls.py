from django.urls import path, include
from rest_framework.routers import DefaultRouter

import api.views as views

router = DefaultRouter()
router.register('users', views.UserAPIViewSet)
router.register('reviews', views.ReviewAPIViewSet)
router.register('comments', views.CommentAPIViewSet)
router.register('tags', views.TagAPIViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:pk>/publications_count/', views.user_publications_count, name='user_publications_count'),
    path('users/<int:pk>/average_rating/', views.user_average_rating, name='user_average_rating'),
    path('users/<int:pk>/total_likes/', views.user_total_likes, name='user_total_likes'),
    path('users/<int:pk>/comments_count/', views.user_comments_count, name='user_comments_count'),
]