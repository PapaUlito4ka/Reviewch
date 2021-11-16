from functools import reduce

from django.http import HttpRequest, Http404
from django.shortcuts import render
import rest_framework.views as views
import rest_framework.generics as generics
import rest_framework.viewsets as viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import authentication
from django.db.models import Avg
import rest_framework.status as status

from rest_framework.decorators import api_view


import api.serializers as serializers
import core.models as models


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class ReviewAPIViewSet(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer


class CommentAPIViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer


class TagAPIViewSet(viewsets.ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


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
    if user.reviews.count() == 0:
        data = 'empty'
    else:
        data = sum(review.get_average_rating() for review in user.reviews.all()) / user.reviews.count()
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





