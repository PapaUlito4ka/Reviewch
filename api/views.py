from django.http import HttpRequest, Http404
from django.shortcuts import render
import rest_framework.views as views
import rest_framework.generics as generics
import rest_framework.viewsets as viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from django.db.models import Avg, Count
from django.db.models import Prefetch
import rest_framework.status as status

from rest_framework.decorators import api_view
from rest_framework import filters

import api.serializers as serializers
import core.models as models


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'is_staff']
    ordering_fields = ['username']
    ordering = ['username']


class ReviewAPIViewSet(viewsets.ModelViewSet):
    p1 = Prefetch('author')
    p2 = Prefetch('user_ratings')
    p3 = Prefetch('user_likes')
    p4 = Prefetch('comments')
    queryset = models.Review.objects.prefetch_related(p1, p2, p3, p4)\
        .annotate(average_rating=Avg('userreviewrating__rating'))\
        .annotate(likes=Count('user_likes'))
    serializer_class = serializers.ReviewSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'text', 'group',
                     'author__username', 'comments__text']
    ordering_fields = ['-created_at', '-average_rating', '-likes']
    ordering = ['-created_at']

    def create(self, request, *args, **kwargs):
        tags_names = request.data.get('tags', [])
        for tag_name in tags_names:
            models.Tag.objects.get_or_create(name=tag_name)
        return super().create(request, *args, **kwargs)


class CommentAPIViewSet(viewsets.ModelViewSet):
    p1 = Prefetch('author')
    p2 = Prefetch('user_likes')
    p3 = Prefetch('review')
    queryset = models.Comment.objects.prefetch_related(p1, p2, p3)\
        .annotate(likes=Count('user_likes'))
    serializer_class = serializers.CommentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['text', 'author__username']
    ordering_fields = ['-created_at', '-likes']
    ordering = ['-created_at']


class TagAPIViewSet(viewsets.ModelViewSet):
    p1 = Prefetch('reviews')
    queryset = models.Tag.objects.prefetch_related(p1)\
        .annotate(reviews_count=Count('reviews'))
    serializer_class = serializers.TagSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', '-reviews_count']
    ordering = ['-reviews_count']


class UploadImageAPIViewSet(viewsets.ModelViewSet):
    queryset = models.UploadImage.objects.all()
    serializer_class = serializers.UploadImageSerializer

    def create(self, request, *args, **kwargs):
        try:
            request.data['review_id'] = int(request.data['review_id'].read())
            request.data['user_id'] = int(request.data['user_id'].read())
        except:
            pass
        return super().create(request, *args, **kwargs)


def get_user_by_id(pk: int, prefetch: str):
    try:
        return models.User.objects.prefetch_related(prefetch).get(id=pk)
    except models.User.DoesNotExist:
        raise Http404


@api_view(['GET'])
def user_publications_count(request: Request, pk: int):
    user = get_user_by_id(pk, 'reviews')
    return Response({
        'data': user.reviews.count()
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_average_rating(request: Request, pk: int):
    user = get_user_by_id(pk, 'reviews')
    data: str
    if user.reviews.count() == 0:
        data = 'None'
    else:
        if not all(review.get_average_rating() for review in user.reviews.all()):
            data = 'None'
        else:
            data = sum(
                review.get_average_rating()
                for review in user.reviews.all()
                if review.get_average_rating()) / user.reviews.count()
    return Response({
        'data': data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_total_likes(request: Request, pk: int):
    user = get_user_by_id(pk, 'reviews')
    return Response({
        'data': sum(review.get_likes() for review in user.reviews.all())
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_comments_count(request: Request, pk: int):
    user = get_user_by_id(pk, 'comments')
    return Response({
        'data': user.comments.count()
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_profile_reviews(request: Request, pk: int):
    user = get_user_by_id(pk, 'reviews')
    return Response({
        'data': user.reviews
    }, status=status.HTTP_200_OK)




