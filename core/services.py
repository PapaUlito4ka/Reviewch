from typing import Type

from django.http import QueryDict

from api.serializers import DetailUserSerializer, DetailReviewSerializer, CommentSerializer, \
                            UploadImageSerializer, TagSerializer
from core.models import User, Review, Tag, UploadImage


class UserService:

    @staticmethod
    def create(raw_user: Type[QueryDict]):
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

        ImageService.delete(review_id)
        ImageService.create(review_id, files)

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
    def create(review_id: int, files: Type[QueryDict]):
        instances = []
        for image in files.getlist('images'):
            serializer = UploadImageSerializer(data=dict(image=image, review_id=review_id))
            serializer.is_valid(raise_exception=True)
            instances.append(serializer.create(serializer.validated_data))

        return instances

    @staticmethod
    def delete(review_id: int):
        return UploadImage.objects.filter(review_id=review_id).delete()
