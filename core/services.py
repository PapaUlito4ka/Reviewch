from typing import Type, List

from django.http import QueryDict
from rest_framework.exceptions import ValidationError

from api.serializers import DetailUserSerializer, DetailReviewSerializer, CommentSerializer, \
    UploadImageSerializer, TagSerializer
from core.models import User, Review, Tag, UploadImage


class UserService:

    @staticmethod
    def create(raw_user: Type[QueryDict]):
        if isinstance(raw_user, QueryDict):
            raw_user = raw_user.dict()
        serializer = DetailUserSerializer(data=raw_user)
        serializer.is_valid(raise_exception=True)
        return serializer.create(serializer.validated_data)


class ReviewService:

    @staticmethod
    def get(id: int):
        review = Review.objects.get(pk=id)
        serializer = DetailReviewSerializer(instance=review)
        return serializer.data

    @staticmethod
    def create(raw_review: Type[QueryDict]):
        raw_review = raw_review.dict()
        raw_review['tags'] = raw_review['tags'].split()
        raw_review['author_id'] = User.objects.get(username=raw_review['user']).id

        for tag_name in raw_review['tags']:
            TagService.get_or_create(tag_name)

        serializer = DetailReviewSerializer(data=raw_review)
        serializer.is_valid(raise_exception=True)
        return serializer.create(serializer.validated_data)

    @staticmethod
    def update(review_id: int, raw_review: Type[QueryDict], files: Type[QueryDict]):
        raw_review = raw_review.dict()
        raw_review['tags'] = raw_review['tags'].split()
        raw_review['author_id'] = User.objects.get(username=raw_review['user']).id

        for tag_name in raw_review['tags']:
            TagService.get_or_create(tag_name)

        ImageService.update(files, review_id=review_id)

        serializer = DetailReviewSerializer(data=raw_review)
        serializer.is_valid(raise_exception=True)
        review = Review.objects.get(pk=review_id)
        return serializer.update(review, serializer.validated_data)


class CommentService:

    @staticmethod
    def create(raw_comment: Type[QueryDict]):
        raw_comment = raw_comment.dict()
        serializer = CommentSerializer(data=raw_comment)
        serializer.is_valid(raise_exception=True)
        return serializer.create(serializer.validated_data)


class TagService:

    @staticmethod
    def get_or_create(tag_name: str):
        return Tag.objects.get_or_create(name=tag_name)


class ImageService:

    @staticmethod
    def create(files: Type[QueryDict], user_id: int = None, review_id: int = None):
        if (user_id is not None and review_id is not None) or \
                (user_id is None and review_id is None):
            raise ValidationError('only user_id or review_id must be specified')
        instances = []
        for image in files.getlist('images'):
            serializer = None
            if review_id is not None:
                serializer = UploadImageSerializer(data=dict(image=image, review_id=review_id))
            if user_id is not None:
                serializer = UploadImageSerializer(data=dict(image=image, user_id=user_id))
            serializer.is_valid(raise_exception=True)
            instances.append(serializer.create(serializer.validated_data))

        return instances

    @staticmethod
    def update(files: Type[QueryDict], user_id: int = None, review_id: int = None):
        if (user_id is not None and review_id is not None) or \
                (user_id is None and review_id is None):
            raise ValidationError('only user_id or review_id must be specified')
        instances = []
        for image in files.getlist('images'):
            serializer = None
            ins = None
            if review_id is not None:
                serializer = UploadImageSerializer(data=dict(image=image, review_id=review_id))
                ins = UploadImage.objects.get(review_id=review_id)
            if user_id is not None:
                serializer = UploadImageSerializer(data=dict(image=image, user_id=user_id))
                ins = UploadImage.objects.get(user_id=user_id)
            serializer.is_valid(raise_exception=True)
            instances.append(serializer.update(ins, serializer.validated_data))

        return instances

    @staticmethod
    def delete(user_id: int = None, review_id: int = None):
        if (user_id is not None and review_id is not None) or \
                (user_id is None and review_id is None):
            raise ValidationError('only user_id or review_id must be specified')
        if not user_id:
            return UploadImage.objects.filter(review_id=review_id).delete()
        if not review_id:
            return UploadImage.objects.filter(user_id=user_id).delete()
