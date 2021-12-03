from django.http import Http404
import rest_framework.viewsets as viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from django.db.models import Avg, Count
from django.db.models import Prefetch
import rest_framework.status as status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import filters

import api.serializers as serializers
import core.models as models
from api.pagination import UserPagination, ReviewPagination, TagPagination


class UserAPIViewSet(viewsets.ModelViewSet):
    p1 = Prefetch('image')
    queryset = models.User.objects.prefetch_related(p1).all()
    serializer_classes = {
        'list': serializers.ListUserSerializer,
        'retrieve': serializers.DetailUserSerializer
    }
    default_serializer_class = serializers.DetailUserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'is_staff']
    ordering_fields = ['username']
    ordering = ['username']
    pagination_class = UserPagination

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_user_by_id(self, pk: int):
        try:
            return self.queryset.get(id=pk)
        except models.User.DoesNotExist:
            raise Http404

    @action(methods=['get'], detail=True, url_name='publications_count')
    def publications_count(self, request: Request, pk: int = None):
        user = self.get_user_by_id(pk)
        return Response({
            'data': user.reviews.count()
        }, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_name='average_rating')
    def average_rating(self, request: Request, pk: int = None):
        user = self.get_user_by_id(pk)
        data = None

        if all(review.get_average_rating() for review in user.reviews.all()) and \
                user.reviews.count() != 0:
            data = sum(
                review.get_average_rating()
                for review in user.reviews.all()
                if review.get_average_rating()) / user.reviews.count()
        return Response({'data': data}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_name='total_likes')
    def total_likes(self, request: Request, pk: int = None):
        user = self.get_user_by_id(pk)
        return Response({
            'data': sum(review.get_likes() for review in user.reviews.all())
        }, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_name='comments_count')
    def comments_count(self, request: Request, pk: int = None):
        user = self.get_user_by_id(pk)
        return Response({
            'data': user.comments.count()
        }, status=status.HTTP_200_OK)


class ReviewAPIViewSet(viewsets.ModelViewSet):
    p1 = Prefetch('author')
    p2 = Prefetch('user_ratings')
    p3 = Prefetch('user_likes')
    p4 = Prefetch('comments')
    p5 = Prefetch('tags')
    p6 = Prefetch('images')
    queryset = models.Review.objects.prefetch_related(p1, p2, p3, p4, p5, p6) \
        .annotate(average_rating=Avg('userreviewrating__rating')) \
        .annotate(likes=Count('user_likes'))
    serializer_classes = {
        'list': serializers.ListReviewSerializer,
        'retrieve': serializers.DetailReviewSerializer
    }
    default_serializer_class = serializers.DetailReviewSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['group', 'tags__name', 'author__username', 'author__id']
    search_fields = ['title', 'text', 'comments__text']
    ordering_fields = ['created_at', 'average_rating', 'likes']
    ordering = ['-created_at']
    pagination_class = ReviewPagination

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def create(self, request, *args, **kwargs):
        tags_names = request.data.get('tags', [])
        for tag_name in tags_names:
            models.Tag.objects.get_or_create(name=tag_name)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        ins = self.get_object()
        tags_names = request.data.get('tags', [])
        for tag_name in tags_names:
            models.Tag.objects.get_or_create(name=tag_name)
        models.UploadImage.objects.filter(review_id=ins.id).delete()
        return super().update(request, *args, **kwargs)

    def get_review_by_id(self, pk: int):
        try:
            return self.queryset.get(pk=pk)
        except models.Review.DoesNotExist:
            raise Http404

    @action(methods=['put'], detail=True, url_name='like')
    def like(self, request: Request, pk: int = None):
        user = models.User.objects.get(id=request.data.get('user_id'))
        review = self.get_review_by_id(pk)
        try:
            review.user_likes.get(id=user.id)
        except:
            # like
            review.user_likes.add(user)
            return Response(data={'data': review.get_likes()}, status=status.HTTP_200_OK)
        else:
            # remove like
            review.user_likes.remove(user)
            return Response(data={'data': review.get_likes()}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_name='has_like')
    def has_liked(self, request: Request, pk: int = None):
        review = self.get_review_by_id(pk)
        user = models.User.objects.get(id=request.query_params.get('user_id'))
        try:
            review.user_likes.get(id=user.id)
        except:
            return Response(data={'data': False}, status=status.HTTP_200_OK)
        else:
            return Response(data={'data': True}, status=status.HTTP_200_OK)

    @action(methods=['put'], detail=True, url_name='rate')
    def rate(self, request: Request, pk: int = None):
        user = models.User.objects.get(id=request.data.get('user_id'))
        rating = request.data.get('rating')
        review = self.get_review_by_id(pk)
        try:
            user_to_review = review.user_ratings.get(
                userreviewrating__user_id=user.id,
                userreviewrating__review_id=review.id
            )
        except:
            # rate
            user_to_review = models.UserReviewRating(
                user_id=user.id,
                review_id=review.id,
                rating=rating
            )
            user_to_review.save()
            return Response(data={'data': review.get_average_rating()}, status=status.HTTP_200_OK)
        else:
            # remove rate
            review.user_ratings.remove(user_to_review)
            return Response(data={'data': review.get_average_rating()}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_name='has_rated')
    def has_rated(self, request: Request, pk: int = None):
        review = self.get_review_by_id(pk)
        user = models.User.objects.get(id=request.query_params.get('user_id'))
        try:
            user_to_review = models.UserReviewRating.objects.get(
                review=review,
                user=user
            )
        except:
            return Response(data={'data': None}, status=status.HTTP_200_OK)
        else:
            return Response(data={'data': user_to_review.rating}, status=status.HTTP_200_OK)


class CommentAPIViewSet(viewsets.ModelViewSet):
    p1 = Prefetch('author')
    p2 = Prefetch('user_likes')
    p3 = Prefetch('review')
    queryset = models.Comment.objects.prefetch_related(p1, p2, p3) \
        .annotate(likes=Count('user_likes'))
    serializer_class = serializers.CommentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['text', 'author__username']
    ordering_fields = ['created_at', 'likes']
    ordering = ['-created_at']

    def get_comment_by_id(self, pk: int):
        try:
            return self.queryset.get(pk=pk)
        except models.Review.DoesNotExist:
            raise Http404

    @action(methods=['put'], detail=True, url_name='like')
    def like(self, request: Request, pk: int = None):
        user = models.User.objects.get(id=request.data.get('user_id'))
        comment = self.get_comment_by_id(pk)
        try:
            comment.user_likes.get(id=user.id)
        except:
            # like
            comment.user_likes.add(user)
            return Response(data={'data': comment.get_likes()}, status=status.HTTP_200_OK)
        else:
            # dislike
            comment.user_likes.remove(user)
            return Response(data={'data': comment.get_likes()}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_name='has_liked')
    def has_liked(self, request: Request, pk: int = None):
        user = models.User.objects.get(id=request.query_params.get('user_id'))
        comment = self.get_comment_by_id(pk)
        try:
            comment.user_likes.get(id=user.id)
        except:
            return Response(data={'data': False}, status=status.HTTP_200_OK)
        else:
            return Response(data={'data': True}, status=status.HTTP_200_OK)


class TagAPIViewSet(viewsets.ModelViewSet):
    p1 = Prefetch('reviews')
    queryset = models.Tag.objects.prefetch_related(p1) \
        .annotate(reviews_count=Count('reviews'))
    serializer_class = serializers.TagSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'reviews_count']
    ordering = ['-reviews_count']
    pagination_class = TagPagination

    @action(methods=['get'], detail=False, url_name='names')
    def names(self, request: Request):
        return Response({
            'data': [tag.name for tag in self.queryset]
        }, status=status.HTTP_200_OK)


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
