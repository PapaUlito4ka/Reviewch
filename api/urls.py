from django.urls import path, include
from rest_framework.routers import DefaultRouter

import api.views as views

router = DefaultRouter()
router.register('users', views.UserAPIViewSet)
router.register('reviews', views.ReviewAPIViewSet)
router.register('comments', views.CommentAPIViewSet)
router.register('tags', views.TagAPIViewSet)
router.register('upload_images', views.UploadImageAPIViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
